import pytest
from unittest.mock import Mock

from src.aplication.services.event_processing_service import EventProcessingService
from src.aplication.services.event_enricher import EventEnricher
from src.domain.validators.event_validator import EventValidator
from src.infrastructure.aws.s3.s3_event_repository import S3EventRepository


class TestEventProcessingService:
    @pytest.fixture
    def mock_validator(self):
        return Mock(spec=EventValidator)

    @pytest.fixture
    def mock_enricher(self):
        return Mock(spec=EventEnricher)

    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=S3EventRepository)

    @pytest.fixture
    def service(self, mock_validator, mock_enricher, mock_repository):
        return EventProcessingService(mock_validator, mock_enricher, mock_repository)

    @pytest.fixture
    def sample_event(self):
        return {
            "event_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "ORDER_CREATED",
            "timestamp": "2024-01-01T12:00:00Z",
            "order_id": "ORD-123",
            "customer_id": "CUST-456",
            "product_id": "PROD-789",
            "quantity": 2,
            "unit_price": "99.99",
            "total_amount": "199.98"
        }

    @pytest.fixture
    def enriched_event(self, sample_event):
        enriched = sample_event.copy()
        enriched["peocessing_metadata"] = {
            "processed_at": "2024-01-01T12:00:00+00:00",
            "processing_source": "ai-data-operations-consumer"
        }
        return enriched

    def test_init_stores_dependencies(self, mock_validator, mock_enricher, mock_repository):
        service = EventProcessingService(mock_validator, mock_enricher, mock_repository)

        assert service.validator == mock_validator
        assert service.enricher == mock_enricher
        assert service.repository == mock_repository

    def test_process_calls_validate(self, service, mock_validator, sample_event):
        service.process(sample_event)

        mock_validator.validate.assert_called_once_with(sample_event)

    def test_process_calls_enrich_after_validate(self, service, mock_enricher, sample_event):
        service.process(sample_event)

        mock_enricher.enrich.assert_called_once_with(sample_event)

    def test_process_calls_save_with_enriched_event(self, service, mock_repository, sample_event, enriched_event):
        mock_enricher = Mock(spec=EventEnricher)
        mock_enricher.enrich.return_value = enriched_event
        service.enricher = mock_enricher

        service.process(sample_event)

        mock_repository.save.assert_called_once_with(enriched_event)

    def test_process_full_workflow(self, service, mock_validator, mock_enricher, mock_repository, sample_event, enriched_event):
        mock_enricher.enrich.return_value = enriched_event

        service.process(sample_event)

        mock_validator.validate.assert_called_once_with(sample_event)
        mock_enricher.enrich.assert_called_once_with(sample_event)
        mock_repository.save.assert_called_once_with(enriched_event)

    def test_process_with_validation_error(self, service, mock_validator, mock_enricher, mock_repository, sample_event):
        from src.aplication.exceptions.event_validation_error import EventValidationError
        mock_validator.validate.side_effect = EventValidationError("Invalid event")

        with pytest.raises(EventValidationError, match="Invalid event"):
            service.process(sample_event)

        mock_enricher.enrich.assert_not_called()
        mock_repository.save.assert_not_called()

    def test_process_with_repository_error(self, service, mock_validator, mock_repository, sample_event, enriched_event):
        mock_enricher = Mock(spec=EventEnricher)
        mock_enricher.enrich.return_value = enriched_event
        service.enricher = mock_enricher

        mock_repository.save.side_effect = ValueError("S3 error")

        with pytest.raises(ValueError, match="S3 error"):
            service.process(sample_event)

        mock_validator.validate.assert_called_once()
        mock_enricher.enrich.assert_called_once()

    def test_process_preserves_event_order(self, service, mock_validator, mock_enricher, mock_repository, sample_event):
        call_order = []

        mock_validator.validate.side_effect = lambda e: call_order.append("validate")
        mock_enricher.enrich.side_effect = lambda e: call_order.append("enrich")
        mock_repository.save.side_effect = lambda e: call_order.append("save")

        service.process(sample_event)

        assert call_order == ["validate", "enrich", "save"]