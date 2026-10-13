from src.entrypoint.lambda_handler import handler
import os

os.environ["RAW_BUCKET_NAME"] = "ai-data-operations-event-processor-raw"

from src.entrypoint.lambda_handler import handler
import os
import base64
import json

os.environ["RAW_BUCKET_NAME"] = "ai-data-operations-event-processor-raw"

# Payload do evento com event_version
payload = {
    "event_id": "123e4567-e89b-12d3-a456-426614174000",
    "event_type": "ORDER_CREATED",
    "timestamp": "2026-10-12T20:36:37.514831+00:00",
    "order_id": "ORD-123",
    "customer_id": "CUST-456",
    "product_id": "PROD-789",
    "quantity": 2,
    "unit_price": 99.99,
    "total_amount": 199.98,
    "event_version": 1
}

# Converter para base64
encoded_data = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")

evento = {
  "Records": [
    {
      "kinesis": {
        "data": encoded_data,
        "sequenceNumber": "123456789",
        "partitionKey": "partition-1"
      },
      "eventID": "shardId-000000000000:123456789",
      "eventSourceARN": "arn:aws:kinesis:us-east-2:123456789012:stream/ai-data-operations-events",
      "eventSource": "aws:kinesis",
      "awsRegion": "us-east-2",
      "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-role"
    }
  ]
}

print("Iniciando execução local...")
handler(evento, None)

