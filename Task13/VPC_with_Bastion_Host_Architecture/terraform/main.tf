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

resource "aws_vpc" "task13" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "task13-vpc"
  }
}

resource "aws_internet_gateway" "task13" {
  vpc_id = aws_vpc.task13.id

  tags = {
    Name = "task13-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.task13.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "task13-public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.task13.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = false

  tags = {
    Name = "task13-private-subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.task13.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.task13.id
  }

  tags = {
    Name = "task13-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "bastion" {
  name        = "task13-bastion-sg"
  description = "SSH from administrator IP"
  vpc_id      = aws_vpc.task13.id

  ingress {
    description = "SSH from administrator"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "private" {
  name        = "task13-private-sg"
  description = "SSH only from Bastion Security Group"
  vpc_id      = aws_vpc.task13.id

  ingress {
    description     = "SSH from Bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
