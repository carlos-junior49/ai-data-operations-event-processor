# src/aplication/services/event_enricher.py

from typing import Mapping, Dict, Any
from datetime import datetime, timezone


class EventEnricher:
    """Serviço de enriquecimento de eventos"""

    PROCESSING_SOURCE = "ai-data-operations-consumer"

    def enrich(self, event: Mapping[str, Any]) -> Dict[str, Any]:
        """Enriquece o evento com informações de processamento"""
        enriched_event = dict(event)

        enriched_event["peocessing_metadata"] = {
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "processing_source": self.PROCESSING_SOURCE
        }
        return enriched_event