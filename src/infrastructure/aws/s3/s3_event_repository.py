# src/infrastructure/aws/s3/s3_event_repository.py

import json
from typing import Mapping
from typing import Any


class S3EventRepository:
    """Persiste eventos no S3"""

    def __init__(self, bucket_name: str, s3_client: Any):
        if not bucket_name or not bucket_name.strip():
            raise ValueError("O parametro bucket_name deve ser informado")
        self.bucket_name = bucket_name
        self.s3_client = s3_client

    def save(self, event: Mapping[str, Any]) -> None:
        """Serializa e salva o evento no formato json no S3"""
        event_id = event.get("event_id")

        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("O parametro event_id deve ser uma string nao vazia")

        key = f"events/{event_id}.json"

        body = json.dumps(
            event,
            ensure_ascii=False,
            allow_nan=False
        )

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json"
        )
