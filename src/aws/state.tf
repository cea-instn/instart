
terraform {
  backend "s3" {
    key            = "instart.tfstate"
    bucket         = "instart-terraform"
    dynamodb_table = "instart_terraform_state_locks"
    encrypt        = true
  }
}
