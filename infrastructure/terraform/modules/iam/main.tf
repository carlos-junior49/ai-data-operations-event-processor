resource "aws_iam_role" "lambda_execution" {
  name               = var.role_name
  assume_role_policy = file("${path.module}/role.json")
  tags               = var.tags
}

resource "aws_iam_role_policy" "lambda_permissions" {
  name = "${var.role_name}-permissions"
  role = aws_iam_role.lambda_execution.id
  policy = templatefile("${path.module}/policy.json",
    {
      raw_bucket_name    = var.raw_bucket_name
      kinesis_stream_arn = var.kinesis_stream_arn
      failures_queue_arn = var.failures_queue_arn
    }
  )
}
