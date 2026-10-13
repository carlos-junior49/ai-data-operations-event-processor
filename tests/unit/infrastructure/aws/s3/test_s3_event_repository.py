import pytest
from unittest.mock import Mock, MagicMock

from src.infrastructure.aws.s3.s3_event_repository import S3EventRepository


class TestS3EventRepository:
    @pytest.fixture
    def mock_s3_client(self):
        return Mock()

    @pytest.fixture
    def repository(self, mock_s3_client):
        return S3EventRepository("test-bucket", mock_s3_client)

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

    def test_init_with_valid_bucket_name(self, mock_s3_client):
        repo = S3EventRepository("test-bucket", mock_s3_client)
        assert repo.bucket_name == "test-bucket"
        assert repo.s3_client == mock_s3_client

    def test_init_with_empty_bucket_name(self, mock_s3_client):
        with pytest.raises(ValueError, match="O parametro bucket_name deve ser informado"):
            S3EventRepository("", mock_s3_client)

    def test_init_with_whitespace_bucket_name(self, mock_s3_client):
        with pytest.raises(ValueError, match="O parametro bucket_name deve ser informado"):
            S3EventRepository("   ", mock_s3_client)

    def test_init_with_none_bucket_name(self, mock_s3_client):
        with pytest.raises(ValueError, match="O parametro bucket_name deve ser informado"):
            S3EventRepository(None, mock_s3_client)

    def test_save_valid_event(self, repository, mock_s3_client, sample_event):
        repository.save(sample_event)

        mock_s3_client.put_object.assert_called_once()
        call_args = mock_s3_client.put_object.call_args

        assert call_args[1]["Bucket"] == "test-bucket"
        assert call_args[1]["Key"] == "events/123e4567-e89b-12d3-a456-426614174000.json"
        assert call_args[1]["ContentType"] == "application/json"
        assert isinstance(call_args[1]["Body"], bytes)

    def test_save_generates_correct_key(self, repository, mock_s3_client):
        event = {"event_id": "test-event-id"}
        repository.save(event)

        call_args = mock_s3_client.put_object.call_args
        assert call_args[1]["Key"] == "events/test-event-id.json"

    def test_save_with_missing_event_id(self, repository, sample_event):
        del sample_event["event_id"]
        with pytest.raises(ValueError, match="O parametro event_id deve ser uma string nao vazia"):
            repository.save(sample_event)

    def test_save_with_none_event_id(self, repository, sample_event):
        sample_event["event_id"] = None
        with pytest.raises(ValueError, match="O parametro event_id deve ser uma string nao vazia"):
            repository.save(sample_event)

    def test_save_with_empty_event_id(self, repository, sample_event):
        sample_event["event_id"] = ""
        with pytest.raises(ValueError, match="O parametro event_id deve ser uma string nao vazia"):
            repository.save(sample_event)

    def test_save_with_whitespace_event_id(self, repository, sample_event):
        sample_event["event_id"] = "   "
        with pytest.raises(ValueError, match="O parametro event_id deve ser uma string nao vazia"):
            repository.save(sample_event)

    def test_save_with_non_string_event_id(self, repository, sample_event):
        sample_event["event_id"] = 123
        with pytest.raises(ValueError, match="O parametro event_id deve ser uma string nao vazia"):
            repository.save(sample_event)

    def test_save_serializes_json_correctly(self, repository, mock_s3_client, sample_event):
        repository.save(sample_event)

        call_args = mock_s3_client.put_object.call_args
        body = call_args[1]["Body"]
        import json
        decoded = json.loads(body.decode("utf-8"))

        assert decoded["event_id"] == sample_event["event_id"]
        assert decoded["event_type"] == sample_event["event_type"]

    def test_save_uses_utf8_encoding(self, repository, mock_s3_client, sample_event):
        repository.save(sample_event)

        call_args = mock_s3_client.put_object.call_args
        body = call_args[1]["Body"]
        assert isinstance(body, bytes)

    def test_save_with_unicode_characters(self, repository, mock_s3_client):
        event = {"event_id": "test-id", "name": "café"}
        repository.save(event)

        call_args = mock_s3_client.put_object.call_args
        body = call_args[1]["Body"].decode("utf-8")
        assert "café" in body

    def test_save_with_nested_event(self, repository, mock_s3_client):
        event = {
            "event_id": "test-id",
            "metadata": {
                "nested": "value",
                "number": 123
            }
        }
        repository.save(event)

        call_args = mock_s3_client.put_object.call_args
        body = call_args[1]["Body"].decode("utf-8")
        import json
        decoded = json.loads(body)
        assert decoded["metadata"]["nested"] == "value"