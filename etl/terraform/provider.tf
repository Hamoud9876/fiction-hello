
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket = "fiction-hello-etl-state-bucket"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
}

#to pull the output from the core backend state
data "terraform_remote_state" "backend" {
  backend = "s3"
  config = {
    bucket = "fiction-hello-state-bucket"
    key    = "terraform.tfstate" 
    region = "eu-west-2"
  }
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

output "lambda_sg_id" {
  value = aws_security_group.lambda_sg.id
}