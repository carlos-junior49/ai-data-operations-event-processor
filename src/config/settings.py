# src/config/settings.py

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    aws_region: str
    raw_bucket_name: str

    @classmethod
    def from_environment(cls) -> "Settings":
        aws_region = os.getenv("AWS_REGION", "us-east-2")
        raw_bucket_name = os.getenv("RAW_BUCKET_NAME", "").strip()

        if not raw_bucket_name:
            raise ValueError("RAW_BUCKET_NAME é obrigatório.")

        return cls(aws_region, raw_bucket_name)
