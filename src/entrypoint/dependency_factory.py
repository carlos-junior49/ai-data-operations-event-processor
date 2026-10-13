# src/entrypoint/dependency_factory.py

import boto3
from src.aplication.services.event_processing_service import EventProcessingService
from src.aplication.services.event_enricher import EventEnricher
from src.config.settings import Settings
from src.domain.validators.event_validator import EventValidator
from src.infrastructure.aws.s3.s3_event_repository import S3EventRepository


def build_event_processing_service() -> EventProcessingService:
    settings = Settings.from_environment()

    s3_client = boto3.client("s3", region_name=settings.aws_region)
    repository = S3EventRepository(settings.raw_bucket_name, s3_client)

    return EventProcessingService(
        validator=EventValidator(),
        enricher=EventEnricher(),
        repository=repository
    )
