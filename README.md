# EarthOne Upload Lambda

This repository contains an AWS Lambda (container-based) service that:

1. Is triggered by an S3 upload event
2. Downloads imagery + metadata
3. Registers the image in the EarthDaily EarthOne catalog
4. Returns the created EarthOne image ID for downstream processing

---

## 🚀 Architecture

S3 Upload → Lambda → EarthOne Catalog → Step Function / Inference Engine

---

## 📦 Tech Stack

- Python 3.12
- AWS Lambda (Container Image)
- AWS S3
- EarthDaily EarthOne SDK (`earthdaily-earthone`)
- Docker
- uv (optional dependency management)

---

## 🛠️ Setup

### 1. Build Docker Image
docker build -t earthone-upload-lambda .

### 2. Push to ECR
aws ecr create-repository --repository-name earthone-upload-lambda

aws ecr get-login-password --region us-west-2 | docker login \
  --username AWS \
  --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

docker tag earthone-upload-lambda:latest <ecr-repo-uri>:latest
docker push <ecr-repo-uri>:latest
