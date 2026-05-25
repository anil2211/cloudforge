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


COMPLETE AWS NETWORKING + EKS + ECR
PHASE 7 — COMPLETE AWS NETWORKING

Now we will build:

Internet Gateway
Route Tables
Public Routing
NAT Gateway
Private Subnets
Security Groups
EKS-ready networking
IMPORTANT

EKS requires:

Minimum 2 subnets
Different availability zones
Proper route tables
Internet connectivity
STEP 1 — UPDATE main.tf

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "cloudforge-vpc"
  }
}

# PUBLIC SUBNET 1
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
    "kubernetes.io/role/elb" = "1"
  }
}

}

STEP 2 — APPLY TERRAFORM

terraform fmt
terraform validate
terraform plan
terraform apply

VERIFY NETWORKING

Inside AWS Console verify:

VPC

Check:

VPC created
DNS enabled
Subnets

Check:

2 public subnets
2 private subnets
Different AZs
Internet Gateway

Check:

IGW attached to VPC
Route Tables

Check:

Public route table exists
0.0.0.0/0 route exists
SUCCESS CHECKPOINT #5

Verify:

Internet Gateway working
Public subnets created
Private subnets created
Route table attached

ONLY THEN continue.

PHASE 8 — CREATE SECURITY GROUPS
STEP 1 — ADD SECURITY GROUPS

Append this to main.tf
resource "aws_security_group" "eks_nodes" {
  name        = "eks-node-group"
  description = "Security group for EKS nodes"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "eks-node-sg"
  }
}

APPLY TERRAFORM


terraform apply

VERIFY SECURITY GROUP

Inside AWS:

Check:

Security group created
Inbound rules active
SUCCESS CHECKPOINT #6

Verify:

Security group visible
Attached to correct VPC

PHASE 9 — CREATE EKS CLUSTER
IMPORTANT

This phase may take:
STEP 1 — CREATE eks.tf

Create file:eks.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.4"

  cluster_name    = "cloudforge-eks"
  cluster_version = "1.31"

  subnet_ids = [
    aws_subnet.private_1.id,
    aws_subnet.private_2.id
  ]

  vpc_id = aws_vpc.main.id

  eks_managed_node_groups = {
    default = {
      desired_size = 2
      min_size     = 1
      max_size     = 3

      instance_types = ["t3.medium"]

      capacity_type = "ON_DEMAND"
    }
  }
}

STEP 2 — INITIALIZE MODULES
terraform init

STEP 3 — PLAN

terraform plan

STEP 4 — APPLY

terraform apply

VERIFY EKS CLUSTER

Inside AWS:

Open:

EKS

Check:

cluster active
node group active

STEP 5 — CONFIGURE kubectl

aws eks update-kubeconfig --region ap-south-1 --name cloudforge-eks

VERIFY CLUSTER ACCESS

kubectl get nodes
Ready nodes

DEBUGGING COMMANDS
Cluster Info
kubectl cluster-info
Nodes
kubectl get nodes
Pods
kubectl get pods -A

SUCCESS CHECKPOINT #7

Verify:

EKS cluster active
Worker nodes ready
kubectl connected

ONLY THEN continue.

PHASE 10 — CREATE ECR REPOSITORY
STEP 1 — CREATE REPOSITORY

Run:

aws ecr create-repository --repository-name cloudforge-backend

VERIFY ECR
Inside AWS:
Open:
Amazon ECR
Check:
repository visible

STEP 2 — LOGIN TO ECR

Replace:

ACCOUNT_ID

with your AWS account ID.

Run:aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

STEP 3 — BUILD IMAGE

Go to backend repo:

cd ../cloudforge-backend

Build:

docker build -t cloudforge-backend .

STEP 4 — TAG IMAGE

docker tag cloudforge-backend:latest ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/cloudforge-backend:latest

STEP 5 — PUSH IMAGE
docker push ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/cloudforge-backend:latest
VERIFY IMAGE

Inside AWS:
Open:

ECR Repository

Verify:

image visible
SUCCESS CHECKPOINT #8

Verify:

Docker image pushed
ECR repository working
Image visible in AWS

ONLY THEN continue.

NEXT PART — KUBERNETES DEPLOYMENT + INGRESS + DOMAIN + HTTPS
PHASE 11 — KUBERNETES APPLICATION DEPLOYMENT

Now we will:

Deploy backend to EKS
Create Kubernetes Deployment
Create Service
Verify Pods
Verify Networking
Expose application internally

IMPORTANT

Before continuing verify:

kubectl get nodes

You MUST see:

Ready nodes
STEP 1 — OPEN KUBERNETES REPOSITORY
cd ../cloudforge-k8s

STEP 2 — CREATE FILES 

Create:

namespace.yaml
deployment.yaml
service.yaml
STEP 3 — CREATE namespace.yaml
APPLY NAMESPACE
kubectl apply -f namespace.yaml
VERIFY NAMESPACE
kubectl get namespaces

Expected:cloudforge


STEP 4 — CREATE deployment.yaml

IMPORTANT:

Replace:

ACCOUNT_ID

with your AWS account ID.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: cloudforge

spec:
  replicas: 2

  selector:
    matchLabels:
      app: backend

  template:
    metadata:
      labels:
        app: backend

    spec:
      containers:
      - name: backend

        image: ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/cloudforge-backend:latest

        ports:
        - containerPort: 8000

        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"

          limits:
            memory: "512Mi"
            cpu: "500m"

          periodSeconds: 5

STEP 5 — APPLY DEPLOYMENT
kubectl apply -f deployment.yaml
VERIFY DEPLOYMENT
kubectl get deployments -n cloudforge
VERIFY PODS
kubectl get pods -n cloudforge
Expected:

DEBUGGING COMMANDS
Describe Pod
kubectl describe pod POD_NAME -n cloudforge
Logs

SUCCESS CHECKPOINT #9

Verify:

Deployment created
Pods running
No CrashLoopBackOff
Health checks passing

ONLY THEN continue.
PHASE 12 — CREATE KUBERNETES SERVICE
STEP 1 — CREATE service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: cloudforge

spec:
  selector:
    app: backend

  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000

  type: ClusterIP

APPLY SERVICE
kubectl apply -f service.yaml
VERIFY SERVICE
kubectl get svc -n cloudforge

Expected:

TEST INTERNAL CONNECTIVITY

Run temporary pod:

kubectl run test-pod \
--image=busybox \
--restart=Never \
--rm -it -n cloudforge -- sh

Inside pod:

wget -qO- http://backend-service

Expected:

{"message":"CloudForge Platform Running"}

Exit:

SUCCESS CHECKPOINT #10

Verify:

Service created
Internal networking works
Backend reachable

ONLY THEN continue

PHASE 13 — INSTALL NGINX INGRESS CONTROLLER
STEP 1 — ADD HELM REPOSITORY
helm repo add ingress-nginx \
https://kubernetes.github.io/ingress-nginx


STEP 2 — UPDATE HELM
helm repo update

STEP 3 — INSTALL INGRESS CONTROLLER
helm install ingress-nginx \
ingress-nginx/ingress-nginx \
--namespace ingress-nginx \
--create-namespace
VERIFY INGRESS CONTROLLER
kubectl get pods -n ingress-nginx

Expected:Running ingress controller pods

STEP 4 — VERIFY LOAD BALANCER
kubectl get svc -n ingress-nginx

Expected:

EXTERNAL-IP assigned

IMPORTANT:

This may take:

5–10 minutes
SUCCESS CHECKPOINT #11

Verify:

NGINX ingress running
AWS ELB created
External IP assigned

ONLY THEN continue.

PHASE 14 — CREATE INGRESS RESOURCE
STEP 1 — CREATE ingress.yaml

Replace:

api.yourdomain.com

with your real domain.

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backend-ingress
  namespace: cloudforge

  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /

spec:
  ingressClassName: nginx

  rules:
  - host: api.yourdomain.com

    http:
      paths:
      - path: /
        pathType: Prefix

        backend:
          service:
            name: backend-service

            port:
              number: 80


APPLY INGRESS
kubectl apply -f ingress.yaml
VERIFY INGRESS
kubectl get ingress -n cloudforge

Expected:
SUCCESS CHECKPOINT #12

Verify:

Ingress created
ELB attached
DNS name visible
ONLY THEN continue.

PHASE 15 — DOMAIN CONFIGURATION
STEP 1 — BUY DOMAIN

Use:

urlNamecheaphttps://www.namecheap.com
urlGoDaddyhttps://www.godaddy.com

Example:

cloudforge-devops.site
STEP 2 — OPEN ROUTE53
Inside AWS:

Route53
Hosted Zones
Create Hosted Zone

Add your domain.

STEP 3 — UPDATE NAMESERVERS

Copy Route53 nameservers.

Update them inside:

Namecheap or
GoDaddy

STEP 4 — CREATE DNS RECORD

Create:

api.cloudforge-devops.site

Type:

CNAME

Value:

AWS Load Balancer DNS
VERIFY DNS

SUCCESS CHECKPOINT #13

Verify:

Domain resolves
Route53 working
ELB connected

ONLY THEN continue.


PHASE 16 — ENABLE HTTPS TLS
STEP 1 — INSTALL CERT-MANAGER

kubectl apply -f \
https://github.com/cert-manager/cert-manager/releases/download/v1.14.4/cert-manager.yaml

VERIFY CERT-MANAGER
kubectl get pods -n cert-manager

Expected:

Running cert-manager pods
STEP 2 — CREATE cluster-issuer.yaml

eplace:

yourmail@gmail.com

with your email.