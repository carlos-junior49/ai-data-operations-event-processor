# src/aplication/services/event_processing_service.py

from typing import Mapping, Any
from src.aplication.services.event_enricher import EventEnricher
from src.domain.validators.event_validator import EventValidator
from src.infrastructure.aws.s3.s3_event_repository import S3EventRepository


class EventProcessingService:
    """Orquestrador que faz a integração entre os serviços de validação, enriquecimento e persistência."""

    def __init__(
            self,
            validator: EventValidator,
            enricher: EventEnricher,
            repository: S3EventRepository
    ) -> None:
        self.validator = validator
        self.enricher = enricher
        self.repository = repository

    def process(self, event: Mapping[str, Any]) -> None:
        """Valida, enriquece e persiste o evento"""
        self.validator.validate(event)
        enriched_event = self.enricher.enrich(event)
        self.repository.save(enriched_event)
