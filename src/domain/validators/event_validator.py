# src/domain/validators/event_validator.py

from typing import Mapping
from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from src.aplication.exceptions.event_validation_error import EventValidationError


class EventValidator:
    """Valida a estrutura e os dados de um evento do e-commerce"""

    REQUIRED_FIELDS = {
        "event_id",
        "event_type",
        "timestamp",
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "total_amount",
        "event_version"
    }

    ALLOWED_EVENT_TYPES = {
        "ORDER_CREATED",
        "ORDER_PAID",
        "ORDER_CANCELED",
        "ORDER_SHIPPED",
        "ORDER_DELIVERED"
    }

    def validate(self, event: Mapping[str, object]) -> None:
        if not isinstance(event, Mapping):
            raise EventValidationError("Evento deve ser um mapeamento")

        missing_fields = self.REQUIRED_FIELDS - event.keys()
        if missing_fields:
            fields = ",".join(sorted(missing_fields))
            raise EventValidationError(f"Campos obrigatórios faltando: {fields}")
        print(event)
        self._validate_uuid(event["event_id"])
        self._validate_event_type(event["event_type"])

        self._validate_timestamp(event["timestamp"])

        self._validate_non_empty_string(event["order_id"], "order_id")
        self._validate_non_empty_string(event["customer_id"], "customer_id")
        self._validate_non_empty_string(event["product_id"], "product_id")
        self._validate_positive_integer(event["quantity"], "quantity")
        self._validate_decimal(event["unit_price"], "unit_price")
        self._validate_decimal(event["total_amount"], "total_amount")

    @staticmethod
    def _validate_uuid(value: object) -> None:
        if not isinstance(value, str):
            raise EventValidationError("event_id deve ser uma string")
        try:
            UUID(value)
        except (ValueError, TypeError, AttributeError) as exc:
            raise EventValidationError("event_id deve ser um UUID válido") from exc

    @staticmethod
    def _validate_event_type(value: object) -> None:
        if not isinstance(value, str) or value not in EventValidator.ALLOWED_EVENT_TYPES:
            raise EventValidationError("event_type deve ser uma string e um dos tipos: "
                                       ", ".join(EventValidator.ALLOWED_EVENT_TYPES))

    @staticmethod
    def _validate_positive_integer(value: object, field_name: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise EventValidationError(f"{field_name} deve ser um número inteiro não negativo")

    @staticmethod
    def _validate_timestamp(value: object) -> None:
        if not isinstance(value, str):
            raise EventValidationError("timestamp deve ser uma string")

        try:
            parsed_timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise EventValidationError("timestamp deve ser uma string no formato ISO 8601") from exc

        if parsed_timestamp.tzinfo is None:
            raise EventValidationError("timestamp deve estar incluso no timezone")

    @staticmethod
    def _validate_non_empty_string(value: object, field_name: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise EventValidationError(f"{field_name} deve ser uma string não vazia")

    @staticmethod
    def _validate_decimal(value: object, field_name: str) -> None:
        if not isinstance(value, (str, int, float)):
            raise EventValidationError(f"{field_name} deve ser um decimal válido")

        try:
            Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise EventValidationError(f"{field_name} deve ser um decimal válido") from exc