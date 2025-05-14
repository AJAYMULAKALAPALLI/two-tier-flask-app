terraform {
  backend "s3" {
    bucket = "capstonebucket121" # Replace with your actual S3 bucket name
    key    = "EKS-Ajay/terraform.tfstate"
    region = "us-east-2"
  }
}
