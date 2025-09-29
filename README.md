# MLOps Capstone (Starter, No-Stress Guide)

This repo trains a simple model, serves it with FastAPI, containers it, runs CI/CD to Docker Hub, and can deploy on EC2 via Terraform.

## 0) Prereqs
- Python 3.10
- Git & GitHub account (`karima715`)
- Docker & Docker Hub (`karimaji143`)
- (Optional) AWS CLI + account for Terraform

## 1) Setup locally
```bash
git clone https://github.com/karima715/mlops-capstone.git
cd mlops-capstone

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
