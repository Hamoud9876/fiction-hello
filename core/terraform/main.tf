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

provider "aws" {
  region = "eu-west-2"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}


output "instance_public_ip" {
  value = aws_instance.web.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.core.endpoint
}
output "rds_endpoint_olap" {
  value = aws_db_instance.olap.endpoint
}


output "rds_port" {
  value = aws_db_instance.core.port
}
