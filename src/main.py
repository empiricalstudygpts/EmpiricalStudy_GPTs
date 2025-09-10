"""
GPT Store Batch Tester (Python + Playwright)

Pipeline (per request):
1) Visit URL from CSV
2) Find the chat input box
3) Type the question
4) Send the question
5) Wait for and capture the answer
6) Save results (JSONL: gpt_url, question, answer)

Notes
-----
- This script is for compliant testing (no guardrail evasion, no scraping at scale).
- Use visible mode on first run to log in; profile is persisted if --reuse-profile is set.
- Adjust selectors in SELECTORS if the site DOM changes.
"""

from __future__ import annotations
import argparse
import csv
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

from playwright.sync_api import sync_playwright, BrowserContext, Page, TimeoutError as PWTimeout

# -----------------------------
# Configurable selectors & waits
# -----------------------------
class SELECTORS:
    # Chat composer (input)
    INPUT = "footer textarea, form textarea, textarea, div[contenteditable='true'], div[role='textbox']"
    # Primary send button
    SEND_BUTTON = "[data-testid='send-button'], button[data-testid='send-button'], button:has-text('Send'), button[aria-label*='Send']"
    # Assistant message container (for counting & extracting)
    ASSISTANT_MESSAGE = "[data-message-author='assistant'], [data-testid='assistant-message'], div.text-message, div.markdown.prose, div.markdown, .prose"
    # Streaming indicator (optional)
    STREAMING = "[data-testid='spinner'], .result-streaming, .busy"
    # Extra fallback selectors (based on DOM inspection)
    INPUT_FALLBACK = "div._prosemirror-parent, div[role='textbox'], textarea._fallbackTextarea"
    NEW_CHAT = "a[href*='new'], button:has-text('New Chat')"
    MAIN_CTA = "button:has-text('Try'), button:has-text('Start')"
    SUGGESTION_CHIP = "button[role='button'][data-testid*='chip'], .suggestion-chip"
    ANY_MESSAGE = ".text-message, [data-message-author], [data-testid*='message']"

# Timeouts & pacing
NAV_TIMEOUT_MS = 90_000             # navigation timeout
INPUT_TIMEOUT_MS = 25_000           # wait for input to become usable
GENERATION_GRACE_S = 15             # generation/streaming wait cap
IDLE_AFTER_LOAD_S = 2               # small pause after load

@dataclass
class Job:
    gpt_url: str

# -----------------------------
# Utility helpers
# -----------------------------

def ensure_output_dirs(base: Path) -> None:
    (base / "jsonl").mkdir(parents=True, exist_ok=True)


def load_jobs(csv_path: Path) -> List[Job]:
    jobs: List[Job] = []
    with csv_path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            url = (row.get("gpt_url") or "").strip()
            if not url:
                print(f"[warn] skipping row {i}: missing gpt_url")
                continue
            jobs.append(Job(url))
    return jobs


def wait_for_network_quiet(page: Page, quiet_ms: int = 1200, timeout_ms: int = 15_000):
    page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
    time.sleep(quiet_ms / 1000)


def focus_last_visible(page: Page, selectors: list[str]) -> bool:
    for sel in selectors:
        try:
            loc = page.locator(sel)
            cnt = loc.count()
            # iterate from last to first to prefer bottom composer
            for i in range(cnt - 1, -1, -1):
                node = loc.nth(i)
                if node.is_visible():
                    try:
                        node.click(force=True)
                    except Exception:
                        # try focus if click fails
                        try:
                            node.focus()
                        except Exception:
                            pass
                    return True
        except Exception:
            continue
    return False


def count_assistant_messages(page: Page) -> int:
    try:
        # Prefer explicit assistant markers
        cnt = page.locator("[data-message-author='assistant'], [data-testid='assistant-message']").count()
        if cnt > 0:
            return cnt
        # Fallback: count generic message bubbles and try to exclude user-authored ones where marked
        bubbles = page.locator("div.text-message, " + SELECTORS.ANY_MESSAGE)
        return bubbles.count()
    except Exception:
        return 0


def extract_latest_answer(page: Page) -> str:
    sels = [
        "[data-message-author='assistant']",
        "[data-testid='assistant-message']",
        "div.text-message",
        "div.markdown.prose",
        "div.markdown",
        ".prose",
    ]
    for sel in sels:
        nodes = page.locator(sel)
        count = 0
        try:
            count = nodes.count()
        except Exception:
            continue
        if count == 0:
            continue
        # Walk backward to pick the last visible one
        for i in range(count - 1, -1, -1):
            node = nodes.nth(i)
            try:
                if node.is_visible():
                    return node.inner_text()
            except Exception:
                continue
    return ""


def wait_for_generation_to_finish(page: Page, start_time: float) -> None:
    end_by = start_time + GENERATION_GRACE_S
    seen_streaming = False
    while time.time() < end_by:
        try:
            streaming = page.is_visible(SELECTORS.STREAMING)
        except Exception:
            streaming = False
        if streaming:
            seen_streaming = True
        else:
            if seen_streaming:
                return
        time.sleep(0.5)
    return

# -----------------------------
# Core pipeline steps
# -----------------------------

def step_visit_url(page: Page, url: str) -> None:
    print(f"[nav] goto: {url}")
    page.goto(url, timeout=NAV_TIMEOUT_MS)
    wait_for_network_quiet(page)
    time.sleep(IDLE_AFTER_LOAD_S)
    # Retry once if page looks blank/detached
    try:
        _ = page.title()
    except Exception:
        print("[nav] blank page detected, retrying...")
        page.goto(url, timeout=NAV_TIMEOUT_MS)
        wait_for_network_quiet(page)
        time.sleep(IDLE_AFTER_LOAD_S)


def step_find_input(page: Page) -> None:
    print("[input] locating composer…")
    deadline = time.time() + INPUT_TIMEOUT_MS / 1000
    variants = [
        "footer textarea",
        "form textarea",
        SELECTORS.INPUT,
        SELECTORS.INPUT_FALLBACK,
    ]
    while time.time() < deadline:
        # 1) Prefer the last visible input (bottom composer)
        if focus_last_visible(page, variants):
            print("[input] focused bottom composer")
            return
        # 2) Gentle nudges to reveal composer
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        try:
            page.mouse.wheel(0, 1600)
        except Exception:
            pass
        # 3) Try clicking common entry points (landing cards/chips)
        try:
            nc = page.locator(SELECTORS.NEW_CHAT).first
            if nc.is_visible():
                nc.click()
                time.sleep(0.3)
        except Exception:
            pass
        try:
            cta = page.locator(SELECTORS.MAIN_CTA).first
            if cta.is_visible():
                cta.click()
                time.sleep(0.3)
        except Exception:
            pass
        try:
            chip = page.locator(SELECTORS.SUGGESTION_CHIP).first
            if chip.is_visible():
                chip.click()
                time.sleep(0.3)
        except Exception:
            pass
        # 4) Click near bottom-center as a last resort (often focuses the composer)
        try:
            box = page.viewport_size or {"width": 1200, "height": 800}
            x = int(box["width"] * 0.5)
            y = int(box["height"] * 0.92)
            page.mouse.click(x, y)
        except Exception:
            pass
        time.sleep(0.25)
    raise PWTimeout("composer not found in time")


def step_type_question(page: Page, text: str) -> None:
    print("[type] clearing & inserting question…")
    # Clear any existing text
    for combo in ("Meta+A", "Control+A"):
        try:
            page.keyboard.press(combo)
        except Exception:
            pass
    try:
        page.keyboard.press("Backspace")
    except Exception:
        pass
    # Insert full text at once (avoids IME/keypress loss)
    page.keyboard.insert_text(text)
    time.sleep(0.1)


def step_send(page: Page) -> None:
    print("[send] sending…")
    # Try keyboard first
    for key in ("Enter", "Meta+Enter", "Control+Enter"):
        try:
            page.keyboard.press(key)
            return
        except Exception:
            continue
    # Then try primary button
    for sel in (SELECTORS.SEND_BUTTON, "button[aria-label*='Send']", "[data-testid='send']"):
        try:
            btn = page.locator(sel).first
            if btn.is_visible():
                btn.click()
                return
        except Exception:
            continue
    raise PWTimeout("send action could not be triggered")


def step_wait_and_capture_answer(page: Page, before_cnt: int) -> str:
    print("[wait] waiting for reply…")
    end_by = time.time() + GENERATION_GRACE_S
    while time.time() < end_by:
        now_cnt = count_assistant_messages(page)
        if now_cnt > before_cnt:
            break
        time.sleep(0.5)
    if count_assistant_messages(page) == before_cnt:
        time.sleep(2.0)
    t0 = time.time()
    wait_for_generation_to_finish(page, t0)
    answer = extract_latest_answer(page)
    print(f"[wait] captured {len(answer)} chars")
    return answer


def step_save(outdir: Path, job: Job, page: Page, answer_text: str, question: str) -> dict:
    jsonl_path = outdir / "jsonl" / "results_python_SC.jsonl"
    record = {
        "gpt_url": job.gpt_url,
        "question": question,
        "answer": answer_text,
        "ts": int(time.time()),
    }
    append_jsonl(jsonl_path, record)
    return record

# -----------------------------
# Glue
# -----------------------------

def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def safe_name(text: str) -> str:
    return "".join(c for c in text if c.isalnum() or c in ("-", "_")).strip()[:80]


def safe_name_from_url(url: str) -> str:
    try:
        last = url.rstrip("/").split("/")[-1]
        return safe_name(last or "gpt")
    except Exception:
        return "gpt"


def process_job(page: Page, job: Job, outdir: Path, question: str) -> dict:
    step_visit_url(page, job.gpt_url)
    before = count_assistant_messages(page)
    step_find_input(page)
    step_type_question(page, question)
    step_send(page)
    answer = step_wait_and_capture_answer(page, before)
    return step_save(outdir, job, page, answer, question)


def run(input_csv: Path, outdir: Path, head: bool, reuse_profile: bool, min_wait: float, max_wait: float, question: str):
    ensure_output_dirs(outdir)
    jobs = load_jobs(input_csv)
    if not jobs:
        print("No jobs found in CSV.")
        return

    user_data_dir = str(outdir / "user_data") if reuse_profile else None

    with sync_playwright() as p:
        context: BrowserContext = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir or str(outdir / "tmp_profile"),
            headless=not head,
            viewport={"width": 1360, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.new_page()

        # Pre-open first URL to trigger login if needed
        print("If sign-in is required, complete it in the opened browser. Press Enter here to continue…")
        try:
            first = jobs[0].gpt_url
            page.goto(first, timeout=NAV_TIMEOUT_MS)
            wait_for_network_quiet(page)
            time.sleep(IDLE_AFTER_LOAD_S)
        except Exception:
            pass
        try:
            input()
        except EOFError:
            pass

        for idx, job in enumerate(jobs, start=1):
            print(f"\n=== Job {idx}/{len(jobs)} :: {job.gpt_url} ===")
            try:
                record = process_job(page, job, outdir, question)
                print(f"[done] saved result for {job.gpt_url}")
            except PWTimeout as e:
                print(f"[timeout] {e}")
            except Exception as e:
                print(f"[error] {e}")
            # pacing
            time.sleep(random.uniform(min_wait, max_wait))

        context.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV with column: gpt_url")
    ap.add_argument("--output", required=True, help="Output dir for artifacts")
    ap.add_argument("--question", required=True, help="Prompts to attack the GPTs")
    ap.add_argument("--head", action="store_true", help="Visible browser (recommended for first login)")
    ap.add_argument("--reuse-profile", action="store_true", help="Persist login under output/user_data")
    ap.add_argument("--min-wait", type=float, default=10.0, help="Min seconds to wait between jobs")
    ap.add_argument("--max-wait", type=float, default=15.0, help="Max seconds to wait between jobs")
    args = ap.parse_args()

    run(
        input_csv=Path(args.input),
        outdir=Path(args.output),
        head=args.head,
        reuse_profile=args.reuse_profile,
        min_wait=max(0.0, args.min_wait),
        max_wait=max(args.min_wait, args.max_wait),
        question=args.question,
    )


if __name__ == "__main__":
    main()