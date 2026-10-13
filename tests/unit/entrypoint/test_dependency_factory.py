import pytest
from unittest.mock import Mock, patch

from src.entrypoint.dependency_factory import build_event_processing_service
from src.aplication.services.event_processing_service import EventProcessingService
from src.aplication.services.event_enricher import EventEnricher
from src.domain.validators.event_validator import EventValidator
from src.infrastructure.aws.s3.s3_event_repository import S3EventRepository


class TestDependencyFactory:
    @pytest.fixture
    def mock_settings(self):
        settings = Mock()
        settings.aws_region = "us-east-1"
        settings.raw_bucket_name = "test-bucket"
        return settings

    @pytest.fixture
    def mock_s3_client(self):
        return Mock()

    def test_build_event_processing_service_creates_service(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                service = build_event_processing_service()

                assert isinstance(service, EventProcessingService)

    def test_build_event_processing_service_injects_validator(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                service = build_event_processing_service()

                assert isinstance(service.validator, EventValidator)

    def test_build_event_processing_service_injects_enricher(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                service = build_event_processing_service()

                assert isinstance(service.enricher, EventEnricher)

    def test_build_event_processing_service_injects_repository(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                service = build_event_processing_service()

                assert isinstance(service.repository, S3EventRepository)

    def test_build_event_processing_service_calls_settings_from_environment(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment",
                   return_value=mock_settings) as mock_settings_class:
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                build_event_processing_service()

                mock_settings_class.assert_called_once()

    def test_build_event_processing_service_creates_s3_client_with_region(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client) as mock_boto3:
                build_event_processing_service()

                mock_boto3.assert_called_once_with("s3", region_name="us-east-1")

    def test_build_event_processing_service_creates_repository_with_bucket_name(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                with patch("src.entrypoint.dependency_factory.S3EventRepository") as mock_repository_class:
                    build_event_processing_service()

                    mock_repository_class.assert_called_once()
                    call_args = mock_repository_class.call_args
                    assert call_args[0][0] == "test-bucket"

    def test_build_event_processing_service_creates_repository_with_s3_client(self, mock_settings, mock_s3_client):
        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                with patch("src.entrypoint.dependency_factory.S3EventRepository") as mock_repository_class:
                    build_event_processing_service()

                    call_args = mock_repository_class.call_args
                    assert call_args[0][1] == mock_s3_client

    def test_build_event_processing_service_uses_aws_region_from_settings(self, mock_settings, mock_s3_client):
        mock_settings.aws_region = "eu-west-2"

        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client) as mock_boto3:
                build_event_processing_service()

                mock_boto3.assert_called_once_with("s3", region_name="eu-west-2")

    def test_build_event_processing_service_uses_bucket_name_from_settings(self, mock_settings, mock_s3_client):
        mock_settings.raw_bucket_name = "my-custom-bucket"

        with patch("src.entrypoint.dependency_factory.Settings.from_environment", return_value=mock_settings):
            with patch("src.entrypoint.dependency_factory.boto3.client", return_value=mock_s3_client):
                with patch("src.entrypoint.dependency_factory.S3EventRepository") as mock_repository_class:
                    build_event_processing_service()

                    call_args = mock_repository_class.call_args
                    assert call_args[0][0] == "my-custom-bucket"