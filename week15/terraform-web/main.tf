terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Fetch available zones
data "aws_availability_zones" "available" {}

# VPC module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 4.0"

  name = "week15-vpc"
  cidr = "10.0.0.0/16"

  azs             = data.aws_availability_zones.available.names
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  map_public_ip_on_launch = true

  enable_nat_gateway = false
  enable_vpn_gateway = false
}

# Security group module for HTTP traffic
module "web_sg" {
  source  = "terraform-aws-modules/security-group/aws//modules/http-80"

  name   = "web-sg"
  vpc_id = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
}

# Fetch AMI for EC2 instance
data "aws_ami" "amazon_linux" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  owners = ["amazon"]
}

# EC2 instance module
module "web_server" {
  source          = "terraform-aws-modules/ec2-instance/aws"
  name            = "Jordan-web-server"
  ami             = data.aws_ami.amazon_linux.id
  instance_type   = "t2.micro"
  key_name        = "vockey"
  vpc_security_group_ids = [module.web_sg.security_group_id]
  subnet_id       = element(module.vpc.public_subnets, 0)

  user_data = templatefile("${path.module}/init-script.sh", {
    file_content = "Jordan Sexton-Schoenmann"
  })
}

# Output public IP
output "web_server_public_ip" {
  value = module.web_server.public_ip
}