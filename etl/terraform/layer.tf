# Create a build directory with correct Lambda layer structure
resource "null_resource" "build_ingestion_layer" {
  provisioner "local-exec" {
    command = <<EOT
      set -e

      # Remove old build
      rm -rf ${path.module}/../build_ingestion_layer
      mkdir -p ${path.module}/../build_ingestion_layer/python

      # Install dependencies into python/
      pip install -r ${path.module}/../src/lambda_ingestion/requirement_ingestion.txt \
        -t ${path.module}/../build_ingestion_layer/python

      # Copy your ETL Python modules into python/ so imports work
      mkdir -p ${path.module}/../build_ingestion_layer/python/etl/utils
      mkdir -p ${path.module}/../build_ingestion_layer/python/etl/database

      cp ${path.module}/../utils/check_bucket_content.py \
         ${path.module}/../utils/insert_into_bucket.py \
         ${path.module}/../build_ingestion_layer/python/etl/utils/

      cp ${path.module}/../database/db_connection_olap.py \
         ${path.module}/../build_ingestion_layer/python/etl/database/
    EOT
  }

  triggers = {
    hash = sha1(join("", [
      filemd5("${path.module}/../src/lambda_ingestion/requirement_ingestion.txt"),
      filemd5("${path.module}/../utils/check_bucket_content.py"),
      filemd5("${path.module}/../utils/insert_into_bucket.py"),
      filemd5("${path.module}/../database/db_connection_olap.py"),
      timestamp()
    ]))
  }
}

# Zip it up
data "archive_file" "ingestion_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build_ingestion_layer"
  output_path = "${path.module}/../archives/lambda_ingestion/ingestion.zip"
  depends_on  = [null_resource.build_ingestion_layer]
}

# Create the Lambda layer
resource "aws_lambda_layer_version" "ingestion_layer" {
  filename   = data.archive_file.ingestion_layer_zip.output_path
  layer_name = "ingestion_combined_layer"
  compatible_runtimes = ["python3.12"]
  depends_on = [data.archive_file.ingestion_layer_zip]
}