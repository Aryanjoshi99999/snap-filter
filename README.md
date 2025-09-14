# Snap-Filter: A Serverless, Event-Driven Image Processing Pipeline

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Serverless](https://img.shields.io/badge/serverless-%23FD5750.svg?style=for-the-badge&logo=serverless&logoColor=white)

This project is a complete, serverless application built on AWS. It automatically processes images uploaded to an S3 bucket, creating a thumbnail and using AI to generate content tags, which are then stored in a DynamoDB table. The architecture is fully event-driven and decoupled using an SQS queue for maximum resilience and fault tolerance.

---

## Key Features

-   **Fully Serverless:** No servers to manage. The application scales automatically with demand and you only pay for what you use.
-   **Event-Driven & Decoupled:** The architecture uses SQS to decouple the image upload from the processing, making the system asynchronous and resilient.
-   **Fault Tolerance:** Includes a Dead-Letter Queue (DLQ) to automatically capture and isolate "poison pill" messages that fail repeatedly, preventing data loss and allowing for manual debugging.
-   **AI-Powered Content Tagging:** Integrates with Amazon Rekognition to perform object and scene detection on uploaded images.
-   **Automated Image Resizing:** Uses the Pillow library within AWS Lambda to generate thumbnails on the fly.
-   **Infrastructure as Code (IaC):** The entire application stack is defined in an AWS SAM (`template.yaml`) file for automated and repeatable deployments.

---

## Technologies Used

### AWS Services
-   AWS Lambda
-   Amazon S3
-   Amazon SQS (with DLQ)
-   Amazon DynamoDB
-   Amazon Rekognition
-   AWS SAM & CloudFormation
-   AWS IAM

### Key Libraries
-   Python 3.12
-   Boto3 (AWS SDK for Python)
-   Pillow (for image processing)

---

## Setup and Deployment

The entire application is defined in the `template.yaml` file and can be deployed using the AWS SAM CLI.

1.  **Build the application:**
    ```bash
    sam build
    ```
2.  **Deploy to your AWS account:**
    ```bash
    sam deploy --guided
    ```
3.  **Configure S3 to SQS connection:** After deployment, run the necessary AWS CLI commands to set the S3 bucket notification and the SQS queue policy to allow S3 to send messages to the queue.
