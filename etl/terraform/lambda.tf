#archiving the function itself to be shipped
data "archive_file" "ingestion_lambda" {
  type        = "zip"
  source_file = "${path.module}/../src/lambda_ingestion/lambda_ingestion.py"
  output_path = "${path.module}/../archives/lambda_ingestion/lambda_ingestion.zip"
}


#this implementation of the lambda
resource "aws_lambda_function" "ingestion_lambda" {
  filename         = "${path.module}/../archives/lambda_ingestion/lambda_ingestion.zip"
  function_name    = "ingestion"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_ingestion.ingest_data"
  runtime          = "python3.10"
  timeout          = 521
  memory_size      = 1024


  layers =  [aws_lambda_layer_version.ingestion_layer.arn]
 

  environment {
    variables = {
      DB_OLAP_USERNAME= var.DB_OLAP_USERNAME
      DB_OLAP_PASSWORD= var.DB_OLAP_PASSWORD
      DB_OLAP_DATABASE= var.DB_OLAP_DATABASE
      DB_OLAP_HOST= var.DB_OLAP_HOST
      DB_OLAP_PORT= var.DB_OLAP_PORT
    }
  }

  vpc_config {
    subnet_ids         = [
      data.terraform_remote_state.backend.outputs.private1_subnet_id,
      data.terraform_remote_state.backend.outputs.private2_subnet_id
    ]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
  
  tags = {
    Environment = "production"
    Application = "example"
  }
  depends_on = [ data.archive_file.ingestion_lambda ]
}


resource "aws_lambda_function" "lambda_transform" {
  function_name = "lambda-transform"
  package_type  = "Image"
  image_uri     = "452732946735.dkr.ecr.eu-west-2.amazonaws.com/lambda-transform:latest"
  role          = aws_iam_role.lambda_role.arn
  timeout          = 521
  memory_size      = 1024
}