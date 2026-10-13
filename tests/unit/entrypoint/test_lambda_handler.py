import pytest
import base64
import json
from unittest.mock import Mock, patch

from src.entrypoint.lambda_handler import handler


class TestLambdaHandler:
    @pytest.fixture
    def mock_processing_service(self):
        return Mock()

    @pytest.fixture
    def sample_event(self):
        event_data = {
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
        encoded_data = base64.b64encode(json.dumps(event_data).encode("utf-8")).decode("utf-8")
        return {
            "Records": [
                {
                    "kinesis": {
                        "data": encoded_data,
                        "sequenceNumber": "123456789"
                    }
                }
            ]
        }

    @pytest.fixture
    def context(self):
        return Mock()

    def test_handler_with_none_processing_service(self, sample_event, context):
        mock_service = Mock()
        with patch("src.entrypoint.lambda_handler.build_event_processing_service", return_value=mock_service):
            result = handler(sample_event, context, None)

            assert result["processed_count"] == 1
            mock_service.process.assert_called_once()

    def test_handler_processes_single_record(self, sample_event, context, mock_processing_service):
        result = handler(sample_event, context, mock_processing_service)

        assert result["processed_count"] == 1
        mock_processing_service.process.assert_called_once()

    def test_handler_processes_multiple_records(self, context, mock_processing_service):
        event_data = {"event_id": "test-id"}
        encoded_data = base64.b64encode(json.dumps(event_data).encode("utf-8")).decode("utf-8")
        event = {
            "Records": [
                {"kinesis": {"data": encoded_data, "sequenceNumber": "1"}},
                {"kinesis": {"data": encoded_data, "sequenceNumber": "2"}},
                {"kinesis": {"data": encoded_data, "sequenceNumber": "3"}}
            ]
        }

        result = handler(event, context, mock_processing_service)

        assert result["processed_count"] == 3
        assert mock_processing_service.process.call_count == 3

    def test_handler_with_empty_records(self, context, mock_processing_service):
        event = {"Records": []}
        result = handler(event, context, mock_processing_service)

        assert result["processed_count"] == 0
        mock_processing_service.process.assert_not_called()

    def test_handler_with_no_records_key(self, context, mock_processing_service):
        event = {}
        result = handler(event, context, mock_processing_service)

        assert result["processed_count"] == 0
        mock_processing_service.process.assert_not_called()

    def test_handler_decodes_base64_data(self, sample_event, context, mock_processing_service):
        handler(sample_event, context, mock_processing_service)

        call_args = mock_processing_service.process.call_args[0][0]
        assert call_args["event_id"] == "123e4567-e89b-12d3-a456-426614174000"
        assert call_args["event_type"] == "ORDER_CREATED"

    def test_handler_handles_processing_error(self, sample_event, context, mock_processing_service):
        mock_processing_service.process.side_effect = Exception("Processing failed")

        result = handler(sample_event, context, mock_processing_service)

        assert "batchItemFailures" in result
        assert result["batchItemFailures"][0]["itemIdentifier"] == "123456789"

    def test_handler_handles_invalid_base64(self, context, mock_processing_service):
        event = {
            "Records": [
                {"kinesis": {"data": "invalid-base64!", "sequenceNumber": "1"}}
            ]
        }

        result = handler(event, context, mock_processing_service)

        assert "batchItemFailures" in result
        assert result["batchItemFailures"][0]["itemIdentifier"] == "1"
        mock_processing_service.process.assert_not_called()

    def test_handler_handles_invalid_json(self, context, mock_processing_service):
        invalid_json = base64.b64encode(b"not valid json").decode("utf-8")
        event = {
            "Records": [
                {"kinesis": {"data": invalid_json, "sequenceNumber": "1"}}
            ]
        }

        result = handler(event, context, mock_processing_service)

        assert "batchItemFailures" in result
        assert result["batchItemFailures"][0]["itemIdentifier"] == "1"
        mock_processing_service.process.assert_not_called()

    def test_handler_returns_immediately_on_error(self, context, mock_processing_service):
        event_data = {"event_id": "test-id"}
        valid_data = base64.b64encode(json.dumps(event_data).encode("utf-8")).decode("utf-8")
        event = {
            "Records": [
                {"kinesis": {"data": "invalid", "sequenceNumber": "1"}},
                {"kinesis": {"data": valid_data, "sequenceNumber": "2"}},
                {"kinesis": {"data": valid_data, "sequenceNumber": "3"}}
            ]
        }

        result = handler(event, context, mock_processing_service)

        assert "batchItemFailures" in result
        assert result["batchItemFailures"][0]["itemIdentifier"] == "1"
        mock_processing_service.process.assert_not_called()

    def test_handler_with_missing_kinesis_key(self, context, mock_processing_service):
        event = {
            "Records": [
                {}
            ]
        }

        with pytest.raises(KeyError, match="kinesis"):
            handler(event, context, mock_processing_service)

    def test_handler_with_missing_sequence_number(self, context, mock_processing_service):
        event = {
            "Records": [
                {"kinesis": {}}
            ]
        }

        with pytest.raises(KeyError, match="sequenceNumber"):
            handler(event, context, mock_processing_service)

    def test_handler_logs_error_on_exception(self, sample_event, context, mock_processing_service):
        mock_processing_service.process.side_effect = Exception("Test error")

        with patch("src.entrypoint.lambda_handler.logger") as mock_logger:
            handler(sample_event, context, mock_processing_service)

            mock_logger.exception.assert_called_once()
            assert "Falha no processo do evento Kinesis" in mock_logger.exception.call_args[0][0]

    def test_handler_logs_sequence_number(self, sample_event, context, mock_processing_service):
        mock_processing_service.process.side_effect = Exception("Test error")

        with patch("src.entrypoint.lambda_handler.logger") as mock_logger:
            handler(sample_event, context, mock_processing_service)

            call_args = mock_logger.exception.call_args
            assert "123456789" in call_args[0][1]