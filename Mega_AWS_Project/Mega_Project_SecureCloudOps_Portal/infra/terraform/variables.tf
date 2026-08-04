variable "aws_region" { type = string default = "ap-south-1" }
variable "project_name" { type = string default = "securecloudops" }
variable "admin_cidr" { type = string }
variable "key_name" { type = string }
variable "db_username" { type = string default = "appuser" }
variable "db_password" { type = string sensitive = true }
variable "instance_type" { type = string default = "t3.small" }
variable "desired_capacity" { type = number default = 2 }
variable "min_size" { type = number default = 2 }
variable "max_size" { type = number default = 4 }
