# Environment Setup Notes — DataSieveAi

## Local Environment Verification

This document serves as proof that the local development environment is correctly configured for Data Science work on the DataSieveAi project.

---

## Python Installation

| Field   | Value                          |
|---------|-------------------------------|
| Version | Python 3.13.3                 |
| Source  | python.org (system install)   |
| Command | `python --version`            |

**Verified ✅**

---

## Anaconda / Conda Installation

| Field   | Value                                                         |
|---------|---------------------------------------------------------------|
| Tool    | Anaconda (with conda package manager)                        |
| Purpose | Reproducible environments for DS/ML work                     |
| Config  | Environment defined in `environment.yml`                      |

To create and activate the project environment:
```bash
conda env create -f environment.yml
conda activate datasieveai
```

---

## Installed Packages (system Python)

| Package    | Version |
|------------|---------|
| numpy      | 2.4.3   |
| matplotlib | 3.10.8  |

Additional packages (numpy, pandas, scikit-learn, scipy, jupyter, nltk, spacy, networkx, streamlit) are pinned in `environment.yml` for the conda environment.

---

## Verification Script

Run the included `verify_setup.py` to check your local environment at any time:

```bash
python verify_setup.py
```

This script checks:
- Python version and executable path
- Conda availability
- All core DS/ML packages

---

## How to Reproduce This Environment

```bash
# 1. Clone the repo
git clone https://github.com/<org>/DataSieveAi.git
cd DataSieveAi

# 2. Create the conda environment
conda env create -f environment.yml

# 3. Activate it
conda activate datasieveai

# 4. Verify
python verify_setup.py
```

---

*Branch: `anaconda-installation` | Date: 2026-04-01*
