variable "function_name" {
  description = "The name of the Lambda function."
  type        = string
}

variable "execution_role_arn" {
  description = "The ARN of the IAM role to execute the Lambda function."
  type        = string
}

variable "filename" {
  description = "The path to the Lambda function's deployment package."
  type        = string
}

variable "source_code_hash" {
  description = "The hash of the Lambda function's source code."
  type        = string
}

variable "handler" {
  description = "The Lambda function's handler."
  type        = string
  default     = "src.entrypoint.lambda_handler.handler"
}

variable "runtime" {
  description = "The Lambda function's runtime."
  type        = string
  default     = "python3.12"
}

variable "timeout" {
  description = "The Lambda function's timeout in seconds."
  type        = number
  default     = 60
}

variable "memory_size" {
  description = "The Lambda function's memory size in MB."
  type        = number
  default     = 128
}

variable "raw_bucket_name" {
  description = "The name of the S3 bucket where raw data is stored."
  type        = string
}

variable "kinesis_stream_name" {
  description = "The name of the Kinesis stream."
  type        = string
}

variable "tags" {
  description = "A map of tags to apply to the Lambda function."
  type        = map(string)
  default     = {}
}

variable "lambda_package_patch" {
  description = "The hash of the Lambda function's source code."
  type        = string
}

variable "kinesis_stream_arn" {
  description = "The ARN of the Kinesis stream."
  type        = string
}

variable "failures_queue_arn" {
  description = "The ARN of the SQS queue to store failed records."
  type        = string
}

variable "alert_topic_arn" {
  description = "The ARN of the SNS topic to send alerts."
  type        = string
}