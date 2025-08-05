resource "aws_s3_bucket" "etl_ingestion_bucket" {
  bucket = "etl-ingestion-bucket-2025"

  tags = {
    Name        = "etl_ingestion_bucket"
    Environment = "Dev"
  }
}


resource "aws_s3_bucket" "etl_process_bucket" {
  bucket = "etl-process-bucket-2025"

  tags = {
    Name        = "etl_process_bucket"
    Environment = "Dev"
  }
}

