#Author: Jordan Sexton-Schoenmann

#General Description: This script deploys an EC2 instance in AWS with a security group that allows both HTTP and SSH access. It configures the required
#AWS provider, sets up the instance with a specific AMI, and instance type. It also assigns a key pair for SSH access and applies security group rules.

#Comment: This specifies the providers needed for Terraform.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 0.14.9"
}

#Comment: This configures the AWS providers with defaults and the US-East region.

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

#Comment: This defines an EC2 instance resource with specific AMI, instance type, and security groups.

resource "aws_instance" "app_server" {
  ami           = "ami-0866a3c8686eaeeba"
  instance_type = "t2.micro"
  key_name = "vockey"
  vpc_security_group_ids = [aws_security_group.web-sg.id]

#Comment: Assigns tags for easier group management.

  tags = {
    Name = var.instance_name
  }
}

#Comment: Defines a security group for inbound and outbound access through HTTP and SSH and rules for those ports.

resource "aws_security_group" "web-sg" {
  name = "web-sg"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

    ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}