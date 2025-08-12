#helper source that lets lambda assume the role of lambda
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

#creating the role and giving it the lambda document
resource "aws_iam_role" "lambda_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


#creating the document to allow the s3 policies for the lambda
data "aws_iam_policy_document" "s3_document" {
  statement {
    actions = ["s3:PutObject", "s3:GetObject", "s3:ListBucket", "s3:GetObject"]

    resources = [
          "${aws_s3_bucket.etl_ingestion_bucket.arn}/*",
          aws_s3_bucket.etl_ingestion_bucket.arn,
          "${aws_s3_bucket.etl_process_bucket.arn}/*",
          aws_s3_bucket.etl_process_bucket.arn
        ]
  }
}

#creating the document to allow to monitor lambda
data "aws_iam_policy_document" "cw_document" {
  statement {

    actions = ["logs:CreateLogGroup", "logs:DescribeLogStreams"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

  statement {

    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:log-group:*:*"
    ]
  }
}


#connecting the s3 policy document to the iam policy
 resource "aws_iam_policy" "s3_policy" {
    name = "access-to-s3-role"
    policy = data.aws_iam_policy_document.s3_document.json
 }


#connecting the cloadwatch policy document to the iam policy
resource "aws_iam_policy" "cw_policy" {
  name_prefix = "cw-policy-currency-lambda-"
  policy      = data.aws_iam_policy_document.cw_document.json
}


#attaching the s3 policy to the lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}


#attaching the cloadwatch policy to the lambda role
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}


