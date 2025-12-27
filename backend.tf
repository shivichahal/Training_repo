terraform {
  backend "s3" {
    bucket         = "obut-program-console-bucket"   # Bucket should be created before workflow start
    key            = "dev/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
  }
}