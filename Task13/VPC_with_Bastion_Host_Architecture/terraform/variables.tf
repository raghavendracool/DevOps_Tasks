variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "availability_zone" {
  type    = string
  default = "ap-south-1a"
}

variable "admin_cidr" {
  type        = string
  description = "Administrator public IP in CIDR format, for example 203.0.113.10/32"
}
