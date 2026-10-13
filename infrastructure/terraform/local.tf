locals {
  kinesis_stream_arn = "arn:aws:kinesis:${var.aws_region}:${data.aws_caller_identity.current.account_id}:stream/${var.kinesis_stream_name}"
  failures_queue_arn = "arn:aws:sqs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:ai-data-operations-event-processor-failures"
  alert_topic_arn    = "arn:aws:sns:${var.aws_region}:${data.aws_caller_identity.current.account_id}:ai-data-operations-event-processor-alerts"
}