# Create a build directory with correct Lambda ingestion layer structure
resource "null_resource" "build_ingestion_layer" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/../build_ingestion_layer
      mkdir -p ${path.module}/../build_ingestion_layer/python
      pip install -r ${path.module}/../src/lambda_ingestion/requirement_ingestion.txt -t ${path.module}/../build_ingestion_layer/python
      mkdir -p ${path.module}/../build_ingestion_layer/python/etl/utils
      mkdir -p ${path.module}/../build_ingestion_layer/python/etl/database
      cp ${path.module}/../utils/check_bucket_content.py \
         ${path.module}/../utils/insert_into_bucket.py \
         ${path.module}/../utils/convert_to_csv.py \
         ${path.module}/../build_ingestion_layer/python/etl/utils/
      cp ${path.module}/../database/db_connection_olap.py \
         ${path.module}/../build_ingestion_layer/python/etl/database/
      touch ${path.module}/../build_ingestion_layer/python/etl/__init__.py
      touch ${path.module}/../build_ingestion_layer/python/etl/utils/__init__.py
    EOT
  }
  triggers = {
    hash = sha1(join("", [
      filemd5("${path.module}/../src/lambda_ingestion/requirement_ingestion.txt"),
      filemd5("${path.module}/../utils/check_bucket_content.py"),
      filemd5("${path.module}/../utils/insert_into_bucket.py"),
      filemd5("${path.module}/../utils/convert_to_csv.py"),
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
  # description = "Force new version: ${timestamp()}"
  depends_on = [data.archive_file.ingestion_layer_zip]
}


# Create a build directory with correct Lambda ingestion layer structure
resource "null_resource" "build_load_layer" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/../build_load_layer
      mkdir -p ${path.module}/../build_load_layer/python

      pip install -r ${path.module}/../src/lambda_load/requirements_load.txt -t ${path.module}/../build_load_layer/python

      mkdir -p ${path.module}/../build_load_layer/python/etl/utils
      mkdir -p ${path.module}/../build_load_layer/python/etl/database

      cp ${path.module}/../utils/read_parquet_file.py \
         ${path.module}/../utils/load_into_olap.py \
         ${path.module}/../build_load_layer/python/etl/utils/

      touch ${path.module}/../build_load_layer/python/etl/__init__.py
      touch ${path.module}/../build_load_layer/python/etl/utils/__init__.py
    EOT
  }
  triggers = {
    hash = sha1(join("", [
      filemd5("${path.module}/../src/lambda_load/requirements_load.txt"),
      filemd5("${path.module}/../utils/get_bucket_dirs.py"),
      filemd5("${path.module}/../utils/read_parquet_file.py"),
      filemd5("${path.module}/../utils/load_into_olap.py"),
      filemd5("${path.module}/../database/db_connection_olap.py"),
      timestamp()
    ]))
  }
}

# Zip it up
data "archive_file" "load_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build_load_layer"
  output_path = "${path.module}/../archives/lambda_load/load.zip"
  depends_on  = [null_resource.build_load_layer]
}

# Create the Lambda layer
resource "aws_lambda_layer_version" "load_layer" {
  filename   = data.archive_file.load_layer_zip.output_path
  layer_name = "load_combined_layer"
  description = "Force new version: ${timestamp()}"
  depends_on = [data.archive_file.load_layer_zip]
}


