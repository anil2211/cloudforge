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

APPLY ISSUER
kubectl apply -f cluster-issuer.yaml
STEP 3 — UPDATE ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backend-ingress
  namespace: cloudforge

  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rewrite-target: /

spec:
  ingressClassName: nginx

  tls:
  - hosts:
    - api.cloudforge-devops.site

    secretName: cloudforge-tls

  rules:
  - host: api.cloudforge-devops.site

    http:
      paths:
      - path: /
        pathType: Prefix

        backend:
          service:
            name: backend-service

            port:
              number: 80

APPLY UPDATED INGRESS
kubectl apply -f ingress.yaml
VERIFY TLS CERTIFICATE
kubectl get certificate -n cloudforge

Expected:
VERIFY WEBSITE

Open:

https://api.cloudforge-devops.site

Expected:

{"message":"CloudForge Platform Running"}
SUCCESS CHECKPOINT #14

Verify:

HTTPS working
TLS certificate active
Domain live
Backend accessible publicly

THIS IS A MAJOR RECRUITER DEMO MILESTONE.

DEBUGGING COMMANDS
Ingress
kubectl describe ingress backend-ingress -n cloudforge
Certificates
kubectl get certificates -A
Pods
kubectl get pods -A
Services
kubectl get svc -A

NEXT PART — JENKINS CI/CD + GITHUB WEBHOOKS + AUTOMATED DEPLOYMENT
PHASE 17 — PREPARE JENKINS FOR CI/CD

Now we will automate:

GitHub Push
   ↓
Jenkins Trigger
   ↓
Docker Build
   ↓
Docker Push to ECR
   ↓
Kubernetes Deployment

This is one of the MOST important recruiter demonstration sections.

STEP 1 — OPEN JENKINS

Open:

http://EC2_PUBLIC_IP:8080
STEP 2 — INSTALL REQUIRED JENKINS PLUGINS

Go to:

Manage Jenkins
→ Plugins
→ Available Plugins

Install:

Docker Pipeline
GitHub Integration
Pipeline
Kubernetes
AWS Credentials
Blue Ocean
Stage View
SSH Agent

Restart Jenkins.

STEP 3 — INSTALL DOCKER INSIDE JENKINS

Run on EC2:

sudo usermod -aG docker jenkins

Restart:

sudo systemctl restart jenkins
VERIFY DOCKER ACCESS

Run:

sudo su - jenkins

Then:

docker ps

If no permission issue:

Docker access works.

Exit:

exit
SUCCESS CHECKPOINT #15

Verify:

Jenkins running
Plugins installed
Docker accessible from Jenkins

ONLY THEN continue.

PHASE 18 — CONFIGURE JENKINS CREDENTIALS
STEP 1 — ADD AWS CREDENTIALS

Go:

Manage Jenkins
→ Credentials
→ Global
→ Add Credentials

Type:

AWS Credentials

Add:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

ID:

aws-creds
STEP 2 — ADD GITHUB TOKEN

Generate token from:

urlGitHub Personal Access Tokenshttps://github.com/settings/tokens

Permissions:

repo
workflow
admin:repo_hook
Add Token to Jenkins

Go:

Manage Jenkins
→ Credentials
→ Add Credentials

Type:

Secret text

ID:

github-token
SUCCESS CHECKPOINT #16

Verify:

AWS credentials configured
GitHub token configured

ONLY THEN continue.

PHASE 19 — CREATE JENKINS PIPELINE PROJECT
STEP 1 — CREATE NEW ITEM

Inside Jenkins:

New Item
→ Pipeline

Name:

cloudforge-backend-pipeline
STEP 2 — ENABLE GITHUB WEBHOOK

Inside pipeline config:

Enable:

GitHub hook trigger for GITScm polling
STEP 3 — CONNECT GITHUB REPOSITORY

SCM:

Git

Repository:

https://github.com/YOUR_USERNAME/cloudforge-backend.git

Credentials:

github-token

Branch:

main
STEP 4 — CREATE Jenkinsfile

Inside:

cloudforge-backend/

Create:

Jenkinsfile
Jenkinsfile

IMPORTANT:

Replace:

ACCOUNT_ID

with your AWS account ID.

pipeline {
        AWS_REGION = 'ap-south-1'
        ECR_REPO = 'cloudforge-backend'
        IMAGE_TAG = 'latest'
        ACCOUNT_ID = 'ACCOUNT_ID'
        IMAGE_URI = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
    }


    stages {


        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/cloudforge-backend.git'
            }
        }


        stage('Build Docker Image') {
            steps {
                sh 'docker build -t cloudforge-backend .'
            }
        }


        stage('Authenticate ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }


        stage('Tag Docker Image') {
            steps {
                sh 'docker tag cloudforge-backend:latest $IMAGE_URI'
            }
        }


        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_URI'
            }
        }


        stage('Deploy To Kubernetes') {
            steps {
                sh 'kubectl rollout restart deployment backend -n cloudforge'
            }
        }


        stage('Verify Deployment') {
            steps {
                sh 'kubectl get pods -n cloudforge'
            }
        }
    }
}
STEP 5 — PUSH Jenkinsfile TO GITHUB
git add .
git commit -m "added jenkins pipeline"
git push origin main
SUCCESS CHECKPOINT #17

Verify:

Jenkinsfile visible in GitHub
Jenkins project configured

ONLY THEN continue.

PHASE 20 — CONFIGURE GITHUB WEBHOOK
STEP 1 — OPEN GITHUB REPOSITORY

Go:

Settings
→ Webhooks
→ Add Webhook
STEP 2 — ADD WEBHOOK URL

Use:

http://EC2_PUBLIC_IP:8080/github-webhook/

Content type:

application/json

Events:

Just the push event

Save webhook.

STEP 3 — TEST PIPELINE

Modify backend code:

return {
    'message': 'CI/CD Pipeline Working'
}
PUSH CODE
git add .
git commit -m "testing ci cd"
git push origin main
VERIFY PIPELINE

Inside Jenkins verify:

Pipeline automatically triggered
VERIFY DOCKER PUSH

Inside AWS ECR:

Check:

new image pushed
VERIFY KUBERNETES DEPLOYMENT

Run:

kubectl get pods -n cloudforge
VERIFY WEBSITE

Open:

https://api.cloudforge-devops.site

Expected:

{"message":"CI/CD Pipeline Working"}
SUCCESS CHECKPOINT #18

Verify:

GitHub webhook works
Jenkins pipeline auto triggers
Docker image rebuilt
Image pushed to ECR
Kubernetes deployment updated
Website updated automatically

THIS IS A MASSIVE RECRUITER DEMO FEATURE.

PHASE 21 — CREATE SEPARATE KUBERNETES MANIFEST REPOSITORY

Now we improve architecture.

STEP 1 — MOVE YAML FILES

Move:

namespace.yaml
deployment.yaml
service.yaml
ingress.yaml

into:

cloudforge-k8s
STEP 2 — UPDATE JENKINSFILE

Replace deploy stage:

stage('Deploy To Kubernetes') {
    steps {
        sh 'kubectl apply -f ../cloudforge-k8s/'
    }
}
STEP 3 — PUSH CHANGES
git add .
git commit -m "moved k8s manifests"
git push origin main
SUCCESS CHECKPOINT #19

Verify:

Separate k8s repo working
Jenkins can deploy manifests
Pods still healthy

ONLY THEN continue.

PHASE 22 — ENABLE BLUE GREEN DEPLOYMENT STRATEGY

This makes your project look more enterprise-grade.

STEP 1 — UPDATE deployment.yaml

Add:

strategy:
  type: RollingUpdate


  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1

inside deployment spec.

APPLY
kubectl apply -f deployment.yaml
VERIFY ROLLING UPDATE

Push new backend change.

Run:

kubectl rollout status deployment/backend -n cloudforge
SUCCESS CHECKPOINT #20

Verify:

Rolling updates working
Zero downtime deployment
Pods updating safely

ONLY THEN continue.

PHASE 23 — ADD HEALTH MONITORING TO PIPELINE
UPDATE Jenkinsfile

Add stage:

stage('Health Check') {
    steps {
        sh 'curl -f https://api.cloudforge-devops.site/health'
    }
}
VERIFY

Push code.

Verify:

Pipeline passes health checks
SUCCESS CHECKPOINT #21

Verify:

Automated health verification working
Deployment validation automated
DEBUGGING COMMANDS
Jenkins Logs
sudo journalctl -u jenkins -f
Pipeline Logs

Inside Jenkins:

Build Logs
Kubernetes
kubectl get pods -n cloudforge
kubectl logs POD_NAME -n cloudforge
Rollouts
kubectl rollout status deployment/backend -n cloudforge
NEXT PART

The next implementation section should include:

Prometheus Installation
Grafana Dashboards
Node Exporter
kube-state-metrics
Kubernetes Monitoring
CloudWatch Logging
Fluent Bit
Log Aggregation
Lambda Automation
SNS Alerts
DevSecOps
Trivy Scanning
Checkov
tfsec
AI Log Analysis
Incident Notifications


PHASE 24 — PROMETHEUS + GRAFANA MONITORING

Now we will build:

Kubernetes Monitoring
↓
Prometheus
↓
Grafana
↓
Node Metrics
↓
Pod Metrics
↓
Cluster Metrics

This section is EXTREMELY important for DevOps interviews.

STEP 1 — OPEN MONITORING REPOSITORY
cd ../cloudforge-monitoring
STEP 2 — ADD HELM REPOSITORIES
helm repo add prometheus-community \
https://prometheus-community.github.io/helm-charts
helm repo add grafana \
https://grafana.github.io/helm-charts
UPDATE HELM
helm repo update
STEP 3 — CREATE MONITORING NAMESPACE
kubectl create namespace monitoring
VERIFY
kubectl get ns

Expected:

monitoring
PHASE 25 — INSTALL KUBE PROMETHEUS STACK

This installs:

Prometheus
Grafana
AlertManager
Node Exporter
kube-state-metrics
STEP 1 — INSTALL STACK
helm install monitoring prometheus-community/kube-prometheus-stack \
-n monitoring
IMPORTANT

This installation may take:

5–10 minutes
VERIFY PODS
kubectl get pods -n monitoring

Expected:

Running pods
VERIFY SERVICES
kubectl get svc -n monitoring
SUCCESS CHECKPOINT #22

Verify:

Prometheus running
Grafana running
Node exporter running
kube-state-metrics running

ONLY THEN continue.

PHASE 26 — ACCESS GRAFANA
STEP 1 — GET GRAFANA PASSWORD
kubectl get secret \
--namespace monitoring monitoring-grafana \
-o jsonpath="{.data.admin-password}" | base64 --decode ; echo

Save password.

STEP 2 — PORT FORWARD GRAFANA
kubectl port-forward svc/monitoring-grafana \
3000:80 -n monitoring
OPEN GRAFANA

Open:

http://localhost:3000

Login:

Username: admin
Password: <password>
VERIFY DASHBOARDS

Go:

Dashboards

You should see:

Kubernetes Cluster Monitoring
Node Monitoring
Pod Metrics
SUCCESS CHECKPOINT #23

Verify:

Grafana login works
Dashboards visible
Metrics visible

ONLY THEN continue.

PHASE 27 — EXPOSE GRAFANA PUBLICLY
STEP 1 — CREATE grafana-ingress.yaml

Replace:

grafana.yourdomain.com

with your domain.

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: monitoring

  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod

spec:
  ingressClassName: nginx

  tls:
  - hosts:
    - grafana.yourdomain.com

    secretName: grafana-tls

  rules:
  - host: grafana.yourdomain.com

    http:
      paths:
      - path: /
        pathType: Prefix

        backend:
          service:
            name: monitoring-grafana

            port:
              number: 80
APPLY
kubectl apply -f grafana-ingress.yaml
VERIFY
kubectl get ingress -A
OPEN GRAFANA
https://grafana.yourdomain.com
SUCCESS CHECKPOINT #24

Verify:

Grafana accessible publicly
HTTPS working
Dashboards loading

THIS IS A HUGE RECRUITER FEATURE.

PHASE 28 — ENABLE CLOUDWATCH LOGGING

Now we centralize logs.

STEP 1 — CREATE IAM POLICY

Attach to EKS worker nodes:

CloudWatchAgentServerPolicy
VERIFY IAM ROLE

Inside AWS:

IAM
→ Roles
→ EKS Node Role

Verify policy attached.

PHASE 29 — INSTALL FLUENT BIT
STEP 1 — ADD HELM REPOSITORY
helm repo add fluent https://fluent.github.io/helm-charts
UPDATE
helm repo update
STEP 2 — INSTALL FLUENT BIT
helm install fluent-bit fluent/fluent-bit \
-n monitoring
VERIFY PODS
kubectl get pods -n monitoring

Expected:

fluent-bit running
SUCCESS CHECKPOINT #25

Verify:

Fluent Bit running
Logging agents healthy

ONLY THEN continue.

PHASE 30 — VERIFY CLOUDWATCH LOGS

Inside AWS:

Open:

CloudWatch
→ Log Groups

Verify:

EKS logs appearing
Container logs appearing
SUCCESS CHECKPOINT #26

Verify:

Centralized logging working
Pod logs visible in CloudWatch

ONLY THEN continue.

PHASE 31 — CREATE LAMBDA AUTOMATION

Now we add serverless automation.

STEP 1 — CREATE lambda_function.py

Inside new folder:

cloudforge-lambda

Create:

import json

def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': json.dumps('CloudForge Lambda Running')
    }
ZIP FUNCTION
zip function.zip lambda_function.py
STEP 2 — CREATE LAMBDA

Inside AWS:

Lambda
→ Create Function

Use:

Python 3.12

Upload:

function.zip
TEST FUNCTION

Expected:

{
  "statusCode": 200
}
SUCCESS CHECKPOINT #27

Verify:

Lambda working
Test successful

ONLY THEN continue.

PHASE 32 — SNS ALERTING
STEP 1 — CREATE SNS TOPIC

Inside AWS:

SNS
→ Create Topic

Name:

cloudforge-alerts
STEP 2 — CREATE EMAIL SUBSCRIPTION

Add your email.

Confirm subscription.

STEP 3 — CONNECT CLOUDWATCH ALARMS

Create alarms for:

CPU usage
Memory
Pod failures

Action:

Send notification to SNS
SUCCESS CHECKPOINT #28

Verify:

Email alerts received
CloudWatch alarms active

ONLY THEN continue.

PHASE 33 — DEVSECOPS IMPLEMENTATION

Now we add security scanning.

STEP 1 — INSTALL TRIVY

On Jenkins server:

sudo apt install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | \
gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo deb [signed-by=/usr/share/keyrings/trivy.gpg] \
https://aquasecurity.github.io/trivy-repo/deb \
$(lsb_release -sc) main | \
sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install trivy -y
VERIFY
trivy --version
STEP 2 — SCAN DOCKER IMAGE
trivy image cloudforge-backend:latest
SUCCESS CHECKPOINT #29

Verify:

Vulnerability scan working
CVEs detected

ONLY THEN continue.

PHASE 34 — INSTALL tfsec
INSTALL
curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
VERIFY
tfsec --version
SCAN TERRAFORM
cd ../cloudforge-infra

tfsec .
SUCCESS CHECKPOINT #30

Verify:

Terraform security scan working

ONLY THEN continue.

PHASE 35 — INSTALL CHECKOV
INSTALL
pip install checkov
VERIFY
checkov --version
SCAN INFRASTRUCTURE
checkov -d .
SUCCESS CHECKPOINT #31

Verify:

Checkov scanning works
Security reports generated

ONLY THEN continue.

PHASE 36 — ADD SECURITY SCANNING TO JENKINS
UPDATE Jenkinsfile

Add stages BEFORE deployment:

stage('Trivy Scan') {
    steps {
        sh 'trivy image cloudforge-backend:latest'
    }
}
stage('tfsec Scan') {
    steps {
        sh 'cd ../cloudforge-infra && tfsec .'
    }
}
VERIFY

Push code.

Pipeline should execute scans.

SUCCESS CHECKPOINT #32

Verify:

Automated security scanning works
CI pipeline includes DevSecOps

THIS IMPRESSES RECRUITERS A LOT.

PHASE 37 — AI LOG ANALYSIS

Now we add AI-powered observability.

STEP 1 — CREATE ai-log-analyzer.py

Inside:

cloudforge-monitoring

Create:

import re

log_file = "sample.log"

with open(log_file, "r") as file:
    logs = file.readlines()

errors = []

for log in logs:
    if re.search(r'ERROR|CRITICAL|FAILED', log):
        errors.append(log)

print("==== INCIDENT SUMMARY ====")

for error in errors:
    print(error)
CREATE sample.log
INFO Application started
ERROR Database timeout
INFO Request successful
CRITICAL Kubernetes node failure
RUN ANALYZER
python ai-log-analyzer.py

Expected:

ERROR Database timeout
CRITICAL Kubernetes node failure
IMPROVEMENT IDEA

Later integrate:

OpenAI API
Bedrock
Gemini
Slack alerts

This becomes your “AI + DevOps” recruiter differentiator.

SUCCESS CHECKPOINT #33

Verify:

AI log analysis working
Incident extraction working

ONLY THEN continue.

PHASE 38 — INCIDENT NOTIFICATIONS
CREATE INCIDENT SCRIPT
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

print('Incident notification sent')
FUTURE IMPROVEMENTS

Add:

Slack notifications
Microsoft Teams
PagerDuty
Opsgenie