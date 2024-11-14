#Author: Jordan Sexton-Schoenmann

#General Description: This script sets up the infrastructure needed to deploy startEC2 lambda functions on AWS. It configures the workspace in Terraform Cloud,
#specifies the AWS provider, and defines an IAM role for the Lambda function.

#Comment: This configures Terraform cloud workspace settings.

terraform {
  cloud {
    organization = "fall2024-adv-scripting"
    workspaces {
      name = "Jordan-Workspace"
    }
  }

#Comment: This defines the provider and versioning.

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {

  region  = "us-east-1"

}

#Comment: This defines the IAM role data for Lambda function permissions.

data "aws_iam_role" "lab_role" {

  name = "LabRole"

}

#Comment: This defines the Lambda function to start EC2 instances.

resource "aws_lambda_function" "start_lambda"{
    filename = "startEC2.zip"
    function_name = "Jordan_function_StartEC2"
    role = data.aws_iam_role.lab_role.arn
    runtime = "python3.9"
    handler = "startEC2.lambda_handler"
}