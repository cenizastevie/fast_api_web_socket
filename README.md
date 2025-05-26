# fast_api_web_socket

## Description
This repository contains a FastAPI application integrated with AWS services such as API Gateway WebSocket, Lambda, DynamoDB, and ECS Fargate. It provides a WebSocket connection manager and message handling capabilities.

## Prerequisites
- AWS CLI installed and configured with appropriate permissions.
- Docker installed for building container images.
- An S3 bucket to store Lambda function code.

## Deployment Instructions

### Step 1: Manage ECR Repository
1. **Create the ECR Repository**:
   ```bash
   aws cloudformation deploy --template-file ecr_task.yaml --stack-name fastapi-ecr-repo --capabilities CAPABILITY_NAMED_IAM
   ```

2. **Build and Push Docker Image**:
   ```bash
   cd fastapi_app
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 211626350366.dkr.ecr.us-east-1.amazonaws.com
   docker build -t fastapi-repo .
   docker tag fastapi-repo:latest 211626350366.dkr.ecr.us-east-1.amazonaws.com/fastapi-repo:latest
   docker push 211626350366.dkr.ecr.us-east-1.amazonaws.com/fastapi-repo:latest
   ```


### Step 2: Deploy VPC Stack
1. **Deploy the VPC CloudFormation Stack**:
   ```bash
   aws cloudformation deploy --template-file vpc_cloud_formation.yaml --stack-name fastapi-vpc-stack --capabilities CAPABILITY_NAMED_IAM
   ```

### Step 3: Deploy CloudFormation Stack
1. **Deploy the CloudFormation Stack**:
   ```bash
   aws cloudformation deploy --template-file cloud_formation.yaml --stack-name fastapi-websocket-stack --capabilities CAPABILITY_NAMED_IAM
   ```

### Step 3.5: View CloudFormation Changesets
To preview changes before updating the stack:
1. **Create a changeset:**
   ```cmd
   aws cloudformation create-change-set --stack-name fastapi-websocket-stack --template-body file://cloud_formation.yaml --change-set-name preview-changeset --capabilities CAPABILITY_NAMED_IAM
   ```
2. **Describe the changeset:**
   ```cmd
   aws cloudformation describe-change-set --stack-name fastapi-websocket-stack --change-set-name preview-changeset
   ```
3. **(Optional) Execute the changeset:**
   ```cmd
   aws cloudformation execute-change-set --stack-name fastapi-websocket-stack --change-set-name preview-changeset
   ```
4. **(Optional) Delete the changeset if not needed:**
   ```cmd
   aws cloudformation delete-change-set --stack-name fastapi-websocket-stack --change-set-name preview-changeset
   ```

### Step 4: Update the Stack
To update the stack (e.g., after modifying the application or infrastructure):
1. Rebuild and push the Docker image (if applicable).
2. Redeploy the CloudFormation stack:
   ```bash
   aws cloudformation deploy --template-file cloud_formation.yaml --stack-name fastapi-websocket-stack --capabilities CAPABILITY_NAMED_IAM
   ```

### Step 5: Delete Resources
1. **Delete the CloudFormation Stack**:
   ```bash
   aws cloudformation delete-stack --stack-name fastapi-websocket-stack
   ```

2. **Delete the ECR Repository**:
   ```bash
   aws cloudformation delete-stack --stack-name fastapi-ecr-repo
   ```