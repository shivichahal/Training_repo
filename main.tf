

resource "aws_s3_bucket" "my_data_bucket" {
  # The bucket name must be globally unique across all AWS users
  bucket = "my-unique-terraform-bucket-2025-12-26" 

  tags = {
    Name        = "My Terraform Bucket"
    Environment = "Dev"
  }
}


# Optional: Best practice to block public access
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.my_data_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --- NEW LAMBDA CODE ---

# Packs the Python code into a ZIP
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/lambda_function.zip"
}

# Creates the Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "my_lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Creates the Lambda Function
resource "aws_lambda_function" "my_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "my_new_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

resource "aws_lambda_function" "my_lambda_two" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "my_second_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler_two"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}
