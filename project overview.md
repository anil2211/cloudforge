CloudForge Platform — Full Implementation Playbook (Part 1)
Goal

This guide helps you build a recruiter-grade DevOps showcase platform completely from scratch.

You will build:

AWS Infrastructure
Terraform IaC
EC2 DevOps Server
EKS Kubernetes Cluster
Dockerized Backend
Jenkins CI/CD
Monitoring Stack
HTTPS Domain Deployment
DevSecOps Pipeline
AI-based Log Analysis

This document covers:

Exact execution order
Working code
Verification steps
Common issues
Debugging commands
Production-grade setup
IMPORTANT PROJECT RULES
NEVER SKIP VERIFICATION

After every phase:

Verify locally
Verify in AWS Console
Verify using CLI
Verify using browser

ONLY THEN continue.

FINAL REPOSITORY STRUCTURE

Create these repositories:
cloudforge-infra
cloudforge-backend
cloudforge-k8s
cloudforge-cicd
cloudforge-monitoring

LOCAL MACHINE REQUIREMENTS

Install:

Git
Docker Desktop
VS Code
AWS CLI
Terraform
kubectl
Helm
Python 3.12
VERIFY INSTALLATIONS

aws --version
terraform --version
kubectl version --client
helm version
docker --version
python --version

PHASE 1 — AWS ACCOUNT SETUP
STEP 1 — CREATE IAM USER

Inside AWS:

Open IAM
Create User
Attach:

AdministratorAccess

Create Access Keys
Save:
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

STEP 2 — CONFIGURE AWS CLI
aws configure

AWS Access Key ID
AWS Secret Access Key
Region: ap-south-1
Output: json

VERIFY AWS CLI

aws s3 ls
If successful:
No error means AWS CLI works.

PHASE 2 — CREATE PROJECT WORKSPACE
STEP 1 — CREATE ROOT FOLDER

mkdir cloudforge
cd cloudforge

STEP 2 — CLONE REPOSITORIES

git clone YOUR_REPO_URL
cloudforge/
│
├── cloudforge-infra
├── cloudforge-backend
├── cloudforge-k8s
├── cloudforge-cicd
└── cloudforge-monitoring

PHASE 3 — BUILD BACKEND APPLICATION

STEP 1 — OPEN BACKEND REPO

cd cloudforge-backend

STEP 2 — CREATE PYTHON VENV
python -m venv venv

Windows
venv\Scripts\activate

STEP 3 — INSTALL PACKAGES
pip install fastapi uvicorn

STEP 4 — CREATE app.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {
        'message': 'CloudForge Platform Running'
    }

@app.get('/health')
def health():
    return {
        'status': 'healthy'
    }

STEP 5 — CREATE requirements.txt
fastapi
uvicorn

STEP 6 — RUN APPLICATION
uvicorn app:app --reload
http://localhost:8000

{"message":"CloudForge Platform Running"}

VERIFY HEALTH ENDPOINT

http://localhost:8000/health

{
  "status": "healthy"
}

SUCCESS CHECKPOINT #1

Verify:

API works
No Python errors
Health endpoint works



PHASE 4 — DOCKERIZE APPLICATION

STEP 1 — CREATE Dockerfile

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


STEP 2 — BUILD IMAGE
docker build -t cloudforge-backend .

STEP 3 — RUN CONTAINER
docker run -p 8000:8000 cloudforge-backend

VERIFY CONTAINER
http://localhost:8000

DEBUGGING COMMANDS
List Containers
docker ps

Logs
docker logs CONTAINER_ID

Stop Container

docker stop CONTAINER_ID

SUCCESS CHECKPOINT #2

SUCCESS CHECKPOINT #2

Verify:

Docker container running
API accessible
No container crash

PHASE 5 — CREATE EC2 DEVOPS SERVER

This server will host:

Jenkins
Terraform
kubectl
Helm
Docker
AWS CLI

STEP 1 — CREATE EC2 INSTANCE
Inside AWS EC2:
Use:
Ubuntu 22.04
t3.large
30GB SSD

SECURITY GROUP RULES
Port	Purpose
22	SSH
80	HTTP
443	HTTPS
8080	Jenkins
3000	Grafana
9090	Prometheus

STEP 2 — CONNECT EC2

ssh -i key.pem ubuntu@EC2_PUBLIC_IP

STEP 3 — UPDATE SERVER
sudo apt update && sudo apt upgrade -y

STEP 4 — INSTALL DOCKER

sudo apt install docker.io -y

sudo systemctl enable docker
sudo systemctl start docker

sudo usermod -aG docker ubuntu

VERIFY DOCKER
docker --version

STEP 5 — INSTALL AWS CLI

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install

CONFIGURE AWS CLI
aws configure

STEP 6 — INSTALL kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/


VERIFY kubectl
kubectl version --client

STEP 7 — INSTALL TERRAFORM

wget -O- https://apt.releases.hashicorp.com/gpg | \
 gpg --dearmor | \
 sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

 echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
 https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
 sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update

sudo apt install terraform -y

VERIFY TERRAFORM


terraform version

STEP 8 — INSTALL HELM
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

VERIFY HELM
helm version

STEP 9 — INSTALL JENKINS

sudo apt install openjdk-17-jdk -y

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
/usr/share/keyrings/jenkins-keyring.asc > /dev/null

 echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
/etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update

sudo apt install jenkins -y

sudo systemctl enable jenkins
sudo systemctl start jenkins

VERIFY JENKINS

http://EC2_PUBLIC_IP:8080

GET INITIAL PASSWORD
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

SUCCESS CHECKPOINT #3
Verify:

Jenkins opens
Docker installed
Terraform works
kubectl works
Helm works
AWS CLI works

ONLY THEN continue.

PHASE 6 — TERRAFORM INFRASTRUCTURE

STEP 1 — OPEN INFRA REPO
CREATE FILES
main.tf
variables.tf
outputs.tf
provider.tf
terraform.tfvars


provider "aws" {
  region = "ap-south-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "cloudforge-vpc"
  }
}

resource "aws_subnet" "public_1" {
  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.1.0/24"

  availability_zone = "ap-south-1a"

  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
  }
}


STEP 2 — INITIALIZE TERRAFORM
terraform init

STEP 3 — VALIDATE
terraform validate

STEP 4 — PLAN
terraform plan

STEP 5 — APPLY
terraform apply

VERIFY AWS RESOURCES

Inside AWS Console:

Verify:

VPC exists
Subnet exists
SUCCESS CHECKPOINT #4

Verify:

Terraform successful
VPC visible in AWS
Subnet visible
ONLY THEN continue.