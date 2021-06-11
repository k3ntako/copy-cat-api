terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_db_instance" "copy_cat_prod" {
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "12.6"
  instance_class         = "db.t2.micro"
  name                   = var.RDS_DB_NAME
  username               = var.RDS_USERNAME
  password               = var.RDS_PASSWORD
  port = var.RDS_PORT
  skip_final_snapshot    = true
}
