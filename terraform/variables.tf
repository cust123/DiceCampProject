# terraform/variables.tf

variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  default = "myDevOpsKeys"
}

variable "project_name" {
  default = "devops-capstone"
}
