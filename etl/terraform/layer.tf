#creating a directory and installing the ingestion lambda requirements into it
resource "null_resource" "create_packages" {
  provisioner "local-exec" {
    command = <<EOT
    mkdir -p ${path.module}/../packages_ingestion/python
    pip install -r ${path.module}/../src/lambda_ingestion/requirement_ingestion.txt -t ${path.module}/../packages_ingestion/python
    EOT
  }

    triggers = {
    utils_hash = sha1(join("", [
      filemd5("${path.module}/../src/lambda_ingestion/requirement_ingestion.txt"),
      timestamp()
    ]))
  }
}


#orgnizing the files ingestion lambda depends on in a new directory 
#compatable with AWS file structure
resource "null_resource" "utils_ingestion_dep" {
  provisioner "local-exec" {
    command = <<EOT
      mkdir -p "${path.module}/../utils_ingestion_dep/python/etl/utils"
      ls -l "${path.module}/../utils"
      cp "${path.module}/../utils/check_bucket_content.py" \
         "${path.module}/../utils/insert_into_bucket.py" \
         "${path.module}/../utils_ingestion_dep/python/etl/utils/"
      mkdir -p "${path.module}/../utils_ingestion_dep/python/etl/database"
      cp "${path.module}/../database/db_connection_olap.py" \
         "${path.module}/../utils_ingestion_dep/python/etl/database/"
    EOT
  }

  triggers = {
    utils_hash = sha1(join("", [
      filemd5("${path.module}/../utils/check_bucket_content.py"),
      filemd5("${path.module}/../utils/insert_into_bucket.py"),
      filemd5("${path.module}/../database/db_connection_olap.py"),
      timestamp()
    ]))
  }
}


#zipping the ingestion lambda dependencies files
data "archive_file" "ingestion_dep" {
  type        = "zip"
  source_dir = "${path.module}/../utils_ingestion_dep"
  output_path = "${path.module}/../archives/lambda_ingestion/ingestion_dep.zip"
  depends_on = [ null_resource.utils_ingestion_dep ]
}


#creating the layer for the ingestion dependencies files
resource "aws_lambda_layer_version" "ingestions_layers_dep" {
  filename   = "${path.module}/../archives/lambda_ingestion/ingestion_dep.zip"
  layer_name = "ingestion_dep"
  depends_on = [data.archive_file.ingestion_dep]
}


#zipping the ingestion lambda packages files
data "archive_file" "ingestion_packages" {
  type        = "zip"
  source_dir = "${path.module}/../packages_ingestion"
  output_path = "${path.module}/../archives/lambda_ingestion/packages_ingestion.zip"
  depends_on = [ null_resource.create_packages ]
}


#creating the layer for the ingestion dependencies files
resource "aws_lambda_layer_version" "ingestions_layers_packages" {
  filename   = "${path.module}/../archives/lambda_ingestion/packages_ingestion.zip"
  layer_name = "ingestion_packages"
  depends_on = [data.archive_file.ingestion_packages]
}


