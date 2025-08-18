terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket = "fiction-hello-state-bucket"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}

#to pull the output from the core etl state
data "terraform_remote_state" "etl" {
  backend = "s3"
  config = {
    bucket = "fiction-hello-etl-state-bucket"
    key    = "terraform.tfstate" 
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}


output "instance_public_ip" {
  value = aws_instance.web.public_ip
}

output "rds_endpoint_core" {
  value = aws_db_instance.core.endpoint
}

output "rds_endpoint_olap" {
  value = aws_db_instance.olap.endpoint
}

output "rds_sg_id" {
  value = aws_security_group.rds_sg.id
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "private1_subnet_id" {
  value = aws_subnet.private1.id
}

output "private2_subnet_id" {
  value = aws_subnet.private2.id
}

output "private1_subnet_cidr" {
  value = aws_subnet.private1.cidr_block
}

output "private2_subnet_cidr" {
  value = aws_subnet.private2.cidr_block
}