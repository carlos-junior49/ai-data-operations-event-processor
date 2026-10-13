import pytest
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from src.domain.validators.event_validator import EventValidator
from src.aplication.exceptions.event_validation_error import EventValidationError


class TestEventValidator:
    @pytest.fixture
    def validator(self):
        return EventValidator()

    @pytest.fixture
    def valid_event(self):
        return {
            "event_id": str(uuid4()),
            "event_type": "ORDER_CREATED",
            "event_version": 1,
            "timestamp": "2024-01-01T12:00:00Z",
            "order_id": "ORD-123",
            "customer_id": "CUST-456",
            "product_id": "PROD-789",
            "quantity": 2,
            "unit_price": "99.99",
            "total_amount": "199.98"
        }

    def test_validate_valid_event(self, validator, valid_event):
        validator.validate(valid_event)

    def test_validate_event_not_mapping(self, validator):
        with pytest.raises(EventValidationError, match="Evento deve ser um mapeamento"):
            validator.validate("not a mapping")

    def test_validate_event_none(self, validator):
        with pytest.raises(EventValidationError, match="Evento deve ser um mapeamento"):
            validator.validate(None)

    def test_validate_event_list(self, validator):
        with pytest.raises(EventValidationError, match="Evento deve ser um mapeamento"):
            validator.validate([])

    def test_validate_missing_single_field(self, validator, valid_event):
        del valid_event["event_id"]
        with pytest.raises(EventValidationError, match="Campos obrigatórios faltando: event_id"):
            validator.validate(valid_event)

    def test_validate_missing_multiple_fields(self, validator, valid_event):
        del valid_event["event_id"]
        del valid_event["event_type"]
        del valid_event["timestamp"]
        with pytest.raises(EventValidationError, match="Campos obrigatórios faltando: event_id,event_type,timestamp"):
            validator.validate(valid_event)

    def test_validate_invalid_uuid_not_string(self, validator, valid_event):
        valid_event["event_id"] = 123
        with pytest.raises(EventValidationError, match="event_id deve ser uma string"):
            validator.validate(valid_event)

    def test_validate_invalid_uuid_format(self, validator, valid_event):
        valid_event["event_id"] = "not-a-uuid"
        with pytest.raises(EventValidationError, match="event_id deve ser um UUID válido"):
            validator.validate(valid_event)

    def test_validate_invalid_uuid_empty(self, validator, valid_event):
        valid_event["event_id"] = ""
        with pytest.raises(EventValidationError, match="event_id deve ser um UUID válido"):
            validator.validate(valid_event)

    def test_validate_event_type_not_string(self, validator, valid_event):
        valid_event["event_type"] = 123
        with pytest.raises(EventValidationError, match="event_type deve ser uma string e um dos tipos"):
            validator.validate(valid_event)

    def test_validate_event_type_invalid(self, validator, valid_event):
        valid_event["event_type"] = "INVALID_TYPE"
        with pytest.raises(EventValidationError, match="event_type deve ser uma string e um dos tipos"):
            validator.validate(valid_event)

    def test_validate_event_type_empty(self, validator, valid_event):
        valid_event["event_type"] = ""
        with pytest.raises(EventValidationError, match="event_type deve ser uma string e um dos tipos"):
            validator.validate(valid_event)

    def test_validate_all_allowed_event_types(self, validator, valid_event):
        for event_type in EventValidator.ALLOWED_EVENT_TYPES:
            valid_event["event_type"] = event_type
            validator.validate(valid_event)

    def test_validate_event_version_valid(self, validator, valid_event):
        valid_event["event_version"] = 1
        validator.validate(valid_event)

    def test_validate_timestamp_not_string(self, validator, valid_event):
        valid_event["timestamp"] = 123
        with pytest.raises(EventValidationError, match="timestamp deve ser uma string"):
            validator.validate(valid_event)

    def test_validate_timestamp_invalid_format(self, validator, valid_event):
        valid_event["timestamp"] = "not-a-timestamp"
        with pytest.raises(EventValidationError, match="timestamp deve ser uma string no formato ISO 8601"):
            validator.validate(valid_event)

    def test_validate_timestamp_no_timezone(self, validator, valid_event):
        valid_event["timestamp"] = "2024-01-01T12:00:00"
        with pytest.raises(EventValidationError, match="timestamp deve estar incluso no timezone"):
            validator.validate(valid_event)

    def test_validate_timestamp_with_timezone(self, validator, valid_event):
        valid_event["timestamp"] = "2024-01-01T12:00:00+00:00"
        validator.validate(valid_event)

    def test_validate_timestamp_with_z(self, validator, valid_event):
        valid_event["timestamp"] = "2024-01-01T12:00:00Z"
        validator.validate(valid_event)

    def test_validate_order_id_not_string(self, validator, valid_event):
        valid_event["order_id"] = 123
        with pytest.raises(EventValidationError, match="order_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_order_id_empty(self, validator, valid_event):
        valid_event["order_id"] = ""
        with pytest.raises(EventValidationError, match="order_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_order_id_whitespace_only(self, validator, valid_event):
        valid_event["order_id"] = "   "
        with pytest.raises(EventValidationError, match="order_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_customer_id_not_string(self, validator, valid_event):
        valid_event["customer_id"] = 123
        with pytest.raises(EventValidationError, match="customer_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_customer_id_empty(self, validator, valid_event):
        valid_event["customer_id"] = ""
        with pytest.raises(EventValidationError, match="customer_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_product_id_not_string(self, validator, valid_event):
        valid_event["product_id"] = 123
        with pytest.raises(EventValidationError, match="product_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_product_id_empty(self, validator, valid_event):
        valid_event["product_id"] = ""
        with pytest.raises(EventValidationError, match="product_id deve ser uma string não vazia"):
            validator.validate(valid_event)

    def test_validate_quantity_not_integer(self, validator, valid_event):
        valid_event["quantity"] = "2"
        with pytest.raises(EventValidationError, match="quantity deve ser um número inteiro não negativo"):
            validator.validate(valid_event)

    def test_validate_quantity_zero(self, validator, valid_event):
        valid_event["quantity"] = 0
        with pytest.raises(EventValidationError, match="quantity deve ser um número inteiro não negativo"):
            validator.validate(valid_event)

    def test_validate_quantity_negative(self, validator, valid_event):
        valid_event["quantity"] = -1
        with pytest.raises(EventValidationError, match="quantity deve ser um número inteiro não negativo"):
            validator.validate(valid_event)

    def test_validate_quantity_boolean_true(self, validator, valid_event):
        valid_event["quantity"] = True
        with pytest.raises(EventValidationError, match="quantity deve ser um número inteiro não negativo"):
            validator.validate(valid_event)

    def test_validate_quantity_valid(self, validator, valid_event):
        valid_event["quantity"] = 5
        validator.validate(valid_event)


    def test_validate_unit_price_invalid_decimal(self, validator, valid_event):
        valid_event["unit_price"] = "not-a-decimal"
        with pytest.raises(EventValidationError, match="unit_price deve ser um decimal válido"):
            validator.validate(valid_event)

    def test_validate_unit_price_invalid_type(self, validator, valid_event):
        valid_event["unit_price"] = None
        with pytest.raises(EventValidationError, match="unit_price deve ser um decimal válido"):
            validator.validate(valid_event)

    def test_validate_unit_price_valid(self, validator, valid_event):
        valid_event["unit_price"] = "99.99"
        validator.validate(valid_event)

    def test_validate_total_amount_invalid_decimal(self, validator, valid_event):
        valid_event["total_amount"] = "not-a-decimal"
        with pytest.raises(EventValidationError, match="total_amount deve ser um decimal válido"):
            validator.validate(valid_event)

    def test_validate_total_amount_valid(self, validator, valid_event):
        valid_event["total_amount"] = "199.98"
        validator.validate(valid_event)

    def test_required_fields_constant(self):
        assert EventValidator.REQUIRED_FIELDS == {
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

    def test_allowed_event_types_constant(self):
        assert EventValidator.ALLOWED_EVENT_TYPES == {
            "ORDER_CREATED",
            "ORDER_PAID",
            "ORDER_CANCELED",
            "ORDER_SHIPPED",
            "ORDER_DELIVERED"
        }