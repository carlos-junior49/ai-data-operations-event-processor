output "role_name" {
  description = "The name of the IAM role."
  value       = aws_iam_role.lambda_execution.name
}

output "role_arn" {
  description = "The ARN of the IAM role."
  value       = aws_iam_role.lambda_execution.arn
}
