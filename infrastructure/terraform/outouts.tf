output "kinesis_stream_name" {
  description = "The name of the Kinesis stream"
  value       = var.kinesis_stream_name
}

output "kinesis_stream_arn" {
  description = "The ARN of the Kinesis stream"
  value       = local.kinesis_stream_arn
}

output "lambda_arn" {
  description = "The ARN of the Lambda function"
  value       = module.lambda.function_arn
}

output "lambda_execution_role_arn" {
  description = "The ARN of the Lambda execution role"
  value       = module.lambda_iam.role_arn
}