variable "role_name" {
  description = "The name of the IAM role."
  type        = string
}

variable "raw_bucket_name" {
  description = "The name of the S3 bucket where raw data will be stored."
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

variable "tags" {
  description = "A map of tags to apply to the IAM role."
  type        = map(string)
  default     = {}
}