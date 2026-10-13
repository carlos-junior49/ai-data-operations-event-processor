resource "aws_lambda_function" "event_processor" {
  function_name    = var.function_name
  role             = var.execution_role_arn
  filename         = var.filename
  source_code_hash = filebase64sha256(var.filename)
  handler          = var.handler
  runtime          = var.runtime
  timeout          = var.timeout
  memory_size      = var.memory_size

  environment {
    variables = {
      RAW_BUCKET_NAME = var.raw_bucket_name
    }
  }

  tags = var.tags

  depends_on = [
    aws_cloudwatch_log_group.lambda
  ]
}

resource "aws_lambda_event_source_mapping" "kinesis" {
  event_source_arn  = var.kinesis_stream_arn
  function_name     = aws_lambda_function.event_processor.arn
  starting_position = "TRIM_HORIZON"
  function_response_types = [
    "ReportBatchItemFailures"
  ]
  batch_size                         = 10
  maximum_batching_window_in_seconds = 300
  maximum_retry_attempts             = 1
  maximum_record_age_in_seconds      = 600

  destination_config {
    on_failure {
      destination_arn = var.failures_queue_arn
    }
  }

  depends_on = [
    aws_lambda_function.event_processor
  ]
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 1

  tags = {
    Environment = "dev"
    Project     = "ai-data-operations"
    ManagedBy   = "terraform"
  }

  lifecycle {
    ignore_changes = all
  }
}

# Alarme 1: erros de execucao da lambda
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${aws_lambda_function.event_processor.function_name}-errors"
  alarm_description   = "Detecta erros na execucao da lambda."
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  datapoints_to_alarm = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [var.alert_topic_arn]

  dimensions = {
    Project     = "ai-data-operations"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

# Alarme 2: throttling da lambda
resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "${aws_lambda_function.event_processor.function_name}-throttles"
  alarm_description   = "Detecta throttling na execucao da lambda."
  namespace           = "AWS/Lambda"
  metric_name         = "Throttles"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  datapoints_to_alarm = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [var.alert_topic_arn]

  dimensions = {
    FunctionName = aws_lambda_function.event_processor.function_name
  }

  tags = {
    Environment = "dev"
    Project     = "ai-data-operations"
    ManagedBy   = "terraform"
  }
}

# Alarme 3: atraso na leitura do Kinesis pela lambda
resource "aws_cloudwatch_metric_alarm" "lambda_iterator_age" {
  alarm_name          = "${aws_lambda_function.event_processor.function_name}-iterator-age"
  namespace           = "AWS/Lambda"
  metric_name         = "IteratorAge"
  statistic           = "Maximum"
  unit                = "Milliseconds"
  period              = 300
  evaluation_periods  = 1
  threshold           = 60000
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [var.alert_topic_arn]

  dimensions = {
    FunctionName = aws_lambda_function.event_processor.function_name
  }

  tags = {
    Environment = "dev"
    Project     = "ai-data-operations"
    ManagedBy   = "terraform"
  }
}