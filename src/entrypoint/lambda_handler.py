# src/entrypoint/lambda_handler.py

import base64
import json
import logging
from typing import Any, Dict, Union
from src.aplication.services.event_processing_service import EventProcessingService
from src.entrypoint.dependency_factory import build_event_processing_service

logger = logging.getLogger(__name__)


def handler(
        event: Dict[str, Any],
        context: Any,
        processing_service: Union[EventProcessingService, None] = None
) -> Dict[str, Any]:
    """Processa batch recebidos do Kinesis."""

    if processing_service is None:
        processing_service = build_event_processing_service()

    records = event.get("Records", [])
    processed_count = 0

    for record in records:
        kinesis_record = record["kinesis"]
        sequence_number = kinesis_record["sequenceNumber"]

        try:
            encoded_data = record.get("kinesis", {}).get("data", "")
            decoded_data = base64.b64decode(encoded_data, validate=True)
            order_event = json.loads(decoded_data)

            processing_service.process(order_event)
            processed_count += 1

        except Exception:
            logger.exception(
                "Falha no processo do evento Kinesis. Sequence number: %s",
                sequence_number
            )

            return {
                "batchItemFailures": [
                    {
                        "itemIdentifier": sequence_number
                    }
                ]
            }

    return {
        "processed_count": processed_count
    }
