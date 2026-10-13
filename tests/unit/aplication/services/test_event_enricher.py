import pytest
from datetime import datetime, timezone
from freezegun import freeze_time

from src.aplication.services.event_enricher import EventEnricher


class TestEventEnricher:
    @pytest.fixture
    def enricher(self):
        return EventEnricher()

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

    def test_enrich_adds_processing_metadata(self, enricher, sample_event):
        with freeze_time("2024-01-01T12:00:00Z"):
            enriched = enricher.enrich(sample_event)

        assert "peocessing_metadata" in enriched
        assert enriched["peocessing_metadata"]["processed_at"] == "2024-01-01T12:00:00+00:00"
        assert enriched["peocessing_metadata"]["processing_source"] == "ai-data-operations-consumer"

    def test_enrich_preserves_original_fields(self, enricher, sample_event):
        enriched = enricher.enrich(sample_event)

        for key, value in sample_event.items():
            assert enriched[key] == value

    def test_enrich_returns_dict(self, enricher, sample_event):
        enriched = enricher.enrich(sample_event)
        assert isinstance(enriched, dict)

    def test_enrich_with_empty_event(self, enricher):
        with freeze_time("2024-01-01T12:00:00Z"):
            enriched = enricher.enrich({})

        assert "peocessing_metadata" in enriched
        assert enriched["peocessing_metadata"]["processed_at"] == "2024-01-01T12:00:00+00:00"
        assert enriched["peocessing_metadata"]["processing_source"] == "ai-data-operations-consumer"

    def test_enrich_with_additional_fields(self, enricher):
        event = {
            "custom_field": "custom_value",
            "another_field": 123
        }
        enriched = enricher.enrich(event)

        assert enriched["custom_field"] == "custom_value"
        assert enriched["another_field"] == 123
        assert "peocessing_metadata" in enriched

    def test_processing_source_constant(self):
        assert EventEnricher.PROCESSING_SOURCE == "ai-data-operations-consumer"

    def test_enrich_does_not_modify_original_event(self, enricher, sample_event):
        original_event = sample_event.copy()
        enricher.enrich(sample_event)

        assert sample_event == original_event
        assert "peocessing_metadata" not in sample_event

    def test_enrich_with_mapping_subclass(self, enricher):
        class CustomMapping(dict):
            pass

        custom_event = CustomMapping({"key": "value"})
        enriched = enricher.enrich(custom_event)

        assert isinstance(enriched, dict)
        assert enriched["key"] == "value"
        assert "peocessing_metadata" in enriched

    def test_enrich_timestamp_format(self, enricher, sample_event):
        with freeze_time("2024-01-01T12:30:45Z"):
            enriched = enricher.enrich(sample_event)

        # Verify ISO format with timezone
        timestamp = enriched["peocessing_metadata"]["processed_at"]
        assert "+" in timestamp or "Z" in timestamp
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))