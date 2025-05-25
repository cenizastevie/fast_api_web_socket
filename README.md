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
   docker build -t fastapi-websocket ./fastapi_app
   docker tag fastapi-websocket:latest <ECR_REPOSITORY_URI>:latest
   docker push <ECR_REPOSITORY_URI>:latest
   ```

3. **Update the CloudFormation template**:
   Ensure the `FastApiTaskDefinition` in `cloud_formation.yaml` references the correct ECR repository URI.

### Step 2: Deploy CloudFormation Stack
1. **Deploy the CloudFormation Stack**:
   ```bash
   aws cloudformation deploy --template-file cloud_formation.yaml --stack-name fastapi-websocket-stack --capabilities CAPABILITY_NAMED_IAM --parameter-overrides VpcId=<VPC_ID> SubnetIds=<SUBNET_IDS>
   ```

### Step 3: Update the Stack
To update the stack (e.g., after modifying the application or infrastructure):
1. Rebuild and push the Docker image (if applicable).
2. Redeploy the CloudFormation stack:
   ```bash
   aws cloudformation deploy --template-file cloud_formation.yaml --stack-name fastapi-websocket-stack --capabilities CAPABILITY_NAMED_IAM
   ```

### Step 4: Delete Resources
1. **Delete the CloudFormation Stack**:
   ```bash
   aws cloudformation delete-stack --stack-name fastapi-websocket-stack
   ```

2. **Delete the ECR Repository**:
   ```bash
   aws cloudformation delete-stack --stack-name fastapi-ecr-repo
   ```