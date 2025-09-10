# An Empirical Study of the Security Vulnerabilities of GPTs

<p align="center">
  <!-- Paper status -->
  <img src="https://img.shields.io/badge/Paper-Under_Review-blue">
  
  <!-- License -->
  <a href="https://creativecommons.org/licenses/by/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg">
  </a>
  
  <!-- DOI -->
  <a href="https://doi.org/10.5281/zenodo.1234567">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg">
  </a>
</p>

## 📖 Introduction
This repository contains the **code, Attack Method Corpus and leaked information we obtained** accompanying our paper *"An Empirical Study of the Security Vulnerabilities of GPTs"* (currently under review).  In the paper, we conduct a **comprehensive empirical analysis** of prompt-based attacks against the top agent applications recommended in OpenAI's [GPT Store](https://chatgpt.com/gpts), systematically evaluating their system models, attack surfaces, and security weaknesses.


Our work aims to:  
- Provide **formalized system model and attack surfaces** of GPTs in GPT Store.
- Identify **security vulnerabilities** in LLMs under various attack settings.  
- Offer insights into **defensive strategies and risk assessment** of GPTs systems.  


## 🧩 Repository Structure
```text
├── attack data/                        
│   ├── results.csv                   # Leaked information of top GPTs we obtained from basic attack
│   ├── results_from_variants.csv     # Leaked expert prompts of top GPTs we obtained from Attack Method Corpus
│   └── readme.md
│
├── defense data/                        
│   ├── defensive_prompts.md             # Defensive prompts used in experiments
│   └── reverse_engineering_GPTs.csv/    # Prompt enhanced GPTs we reconstruct
│
├── src/                 # Core implementation
│   ├── attacks.txt      # Attack prompts
│   ├── gpts_list/       # Different GPTs target lists
│   └── main.py          # Program that launch auto attacks
│
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```


## 🚀 Quick Start

### 0. Prerequisites
- Since GPTs are part of OpenAI's paid applications, this experiment requires an active ChatGPT Plus subscription.
- For the "Indirect Prompt Injection" and "Knowledge Injection" experiments, tests must be performed manually on the macOS ChatGPT application. The verified ChatGPT app version we use in our work is: 1.2025.175 (1751070473)

### 1. Installation

```bash
git clone https://github.com/empiricalstudygpts/EmpiricalStudy_GPTs.git

pip install -r requirements.txt
```

### 2. Running Attacks
```bash
python src/main.py \
  --input src/gpts_list/gpts.csv \          # List of GPTs to be attack
  --output out \              # Output files
  --quesion "..." \           # Attack prompts
  --head --reuse-profile      
```



## ⚠️ Ethical Considerations

This repository is released **for academic research purposes only**. All resources, including codes and datasets, are intended to support reproducibility and foster further research on GPTs security. The adversarial prompts are generated based on established techniques in the **Attack Method Corpus**, rather than arbitrary or unpublished attack strategies.  

- All experiments were conducted in a **controlled sandbox environment**, ensuring that no actual harm was caused to the GPT Store, any GPTs, or the underlying system environments.
- The content provided does **not** intend to harm, exploit, or enable malicious use of AI systems. Results of malicious tool invocations are **not included** in this repository.  
- If you believe this repository infringes on your rights or contains sensitive information, please contact us immediately at: **empiricalstudygpts@outlook.com**. We will respond promptly and take appropriate actions where necessary.  
