terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Starter only: expand with subnets, gateways, route tables, ALB,
# target group, EC2 launch template, ASG, RDS subnet group and RDS.

resource "aws_vpc" "task14" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "task14-vpc"
  }
}
