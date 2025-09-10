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










This is the github repository of paper 《An Empirical Study of the Security Vulnerabilities of GPTs》. 


The res.xlsx shows our results. Each column in the file corresponds to:

the names of GPTs in our experiments,

their leaked expert prompts, 

the names of their jit_plugins / knowledge files, 

the classification of the GPTs based on the components they have (0 means no tools or knowledge, 1 means only basic tools, 2 means only user-defined tools, 3 means basic tools + user-defined tools, 4 means tools + knowledge), 

the results of attacks on three basic tools: DALL·E, Python and browser,

the results knowledge injection attacks on three basic tools: DALL·E, Python and browser,

our proposed prompt-enhanced version of GPTs (E represents including expert prompt defensive tokens, C represents including components defensive tokens, K represents including defensive tokens of separating knowledge instructions).
