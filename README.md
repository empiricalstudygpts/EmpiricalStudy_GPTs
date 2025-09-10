# An Empirical Study of the Security Vulnerabilities of GPTs

<p align="center">
  <img src="https://img.shields.io/badge/Paper-Under_Review-blue">
  <img src="https://img.shields.io/badge/License-MIT-green">
  <img src="https://img.shields.io/badge/Dataset-Available-orange">
</p>

## 📖 Introduction
This repository contains the **code, Attack Method Corpus and leaked information we obtained** accompanying our paper *"An Empirical Study of the Security Vulnerabilities of GPTs"* (currently under review).  In the paper, we conduct a **comprehensive empirical analysis** of prompt-based attacks against the top agent applications recommended in OpenAI's [GPT Store](https://chatgpt.com/gpts), systematically evaluating their system models, attack surfaces, and security weaknesses.


Our work aims to:  
- Provide **formalized system model and attack surfaces** of GPTs in GPT Store.
- Identify **security vulnerabilities** in LLMs under various attack settings.  
- Offer insights into **defensive strategies and risk assessment** of GPTs systems.  


## 🧩 Repository Structure
```text
├── data for attack/                        
│   ├── adversarial prompts/     # Attack prompts used in experiments
│   ├── results/                 # Leaked information of top GPTs we obtained from basic attack
│   └── results from variants/   # Leaked information of top GPTs we obtained from Attack Method Corpus
│
├── data for defenes/                        
│   ├── defensive prompts/           # Defensive prompts used in experiments
│   ├── reverse-engineering GPTs/    # Leaked information of top GPTs we obtained
│   └── metadata.json                # Dataset description
│
├── src/                 # Core implementation
│   ├── attacks/         # Attack algorithms and generation scripts
│   ├── evaluation/      # Evaluation metrics and robustness tests
│   └── utils/           # Helper functions
│
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/your-username/gpt-security-vulnerabilities.git

pip install -r requirements.txt
```

### 2. Running Attacks
```bash
python src/main.py \
  --input gpts.csv \          # List of GPTs to be attack
  --output out \              # Output files
  --quesion "..." \           # Attack prompts
  --head --reuse-profile      
```



## ⚠️ Ethical Considerations

This repository is released **for academic research purposes only**. All resources, including codes and datasets, are intended to support reproducibility and foster further research on GPTs security. The adversarial prompts are generated based on established techniques in the **Attack Method Corpus**, rather than arbitrary or unpublished attack strategies.  

- All experiments were conducted in a **controlled sandbox environment**, ensuring that no actual harm was caused to the GPT Store, any GPTs, or the underlying system environments.
- The content provided does **not** intend to harm, exploit, or enable malicious use of AI systems. Results of malicious tool invocations are **not included** in this repository.  
- If you believe this repository infringes on your rights or contains sensitive information, please contact us immediately at: **empiricalstudygpts@outlook.com**. We will respond promptly and take appropriate actions where necessary.  
