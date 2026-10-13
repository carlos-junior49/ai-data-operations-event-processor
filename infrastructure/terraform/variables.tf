variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
}

variable "raw_bucket_name" {
  description = "The name of the raw data bucket."
  type        = string
}

variable "environment" {
  description = "The environment for which resources will be created."
  type        = string
}

variable "function_name" {
  description = "The name of the Lambda function."
  type        = string
}

variable "lambda_package_patch" {
  description = "The hash of the Lambda function's source code."
  type        = string
}

variable "kinesis_stream_name" {
  description = "The name of the Kinesis stream."
  type        = string
}