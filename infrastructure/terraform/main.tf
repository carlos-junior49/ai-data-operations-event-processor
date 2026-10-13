module "lambda_iam" {
  source = "./modules/iam"

  role_name          = "${var.function_name}-execution-role"
  raw_bucket_name    = var.raw_bucket_name
  kinesis_stream_arn = local.kinesis_stream_arn
  failures_queue_arn = local.failures_queue_arn
}

module "lambda" {
  source = "./modules/lambda"

  function_name        = var.function_name
  raw_bucket_name      = var.raw_bucket_name
  kinesis_stream_name  = var.kinesis_stream_name
  kinesis_stream_arn   = local.kinesis_stream_arn
  execution_role_arn   = module.lambda_iam.role_arn
  lambda_package_patch = var.lambda_package_patch
  filename             = var.lambda_package_patch
  source_code_hash     = filebase64sha256(var.lambda_package_patch)
  failures_queue_arn   = local.failures_queue_arn
  alert_topic_arn      = local.alert_topic_arn
}
