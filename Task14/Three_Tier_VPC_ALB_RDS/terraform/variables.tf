variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "admin_cidr" {
  type        = string
  description = "Administrator public IP in CIDR format"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "RDS master password for training only; prefer Secrets Manager"
}
