import pytest
from unittest.mock import patch
import os

from src.config.settings import Settings


class TestSettings:
    def test_settings_instantiation(self):
        settings = Settings(aws_region="us-east-1", raw_bucket_name="my-bucket")

        assert settings.aws_region == "us-east-1"
        assert settings.raw_bucket_name == "my-bucket"

    def test_settings_is_frozen(self):
        settings = Settings(aws_region="us-east-1", raw_bucket_name="my-bucket")

        with pytest.raises(Exception):  # FrozenInstanceError
            settings.aws_region = "eu-west-1"

    def test_from_environment_with_all_env_vars(self):
        with patch.dict("os.environ", {
            "AWS_REGION": "eu-west-2",
            "RAW_BUCKET_NAME": "test-bucket"
        }):
            settings = Settings.from_environment()

            assert settings.aws_region == "eu-west-2"
            assert settings.raw_bucket_name == "test-bucket"

    def test_from_environment_with_default_aws_region(self):
        with patch.dict("os.environ", {
            "RAW_BUCKET_NAME": "test-bucket"
        }, clear=False):
            # Remove AWS_REGION if it exists to test default
            os.environ.pop("AWS_REGION", None)

            settings = Settings.from_environment()

            assert settings.aws_region == "us-east-2"
            assert settings.raw_bucket_name == "test-bucket"

    def test_from_environment_with_missing_bucket_name(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="RAW_BUCKET_NAME é obrigatório"):
                Settings.from_environment()

    def test_from_environment_with_empty_bucket_name(self):
        with patch.dict("os.environ", {
            "RAW_BUCKET_NAME": ""
        }):
            with pytest.raises(ValueError, match="RAW_BUCKET_NAME é obrigatório"):
                Settings.from_environment()

    def test_from_environment_with_whitespace_bucket_name(self):
        with patch.dict("os.environ", {
            "RAW_BUCKET_NAME": "   "
        }):
            with pytest.raises(ValueError, match="RAW_BUCKET_NAME é obrigatório"):
                Settings.from_environment()

    def test_from_environment_with_whitespace_padded_bucket_name(self):
        with patch.dict("os.environ", {
            "AWS_REGION": "us-east-1",
            "RAW_BUCKET_NAME": "  my-bucket  "
        }):
            settings = Settings.from_environment()

            assert settings.raw_bucket_name == "my-bucket"

    def test_from_environment_with_custom_aws_region(self):
        with patch.dict("os.environ", {
            "AWS_REGION": "ap-southeast-1",
            "RAW_BUCKET_NAME": "test-bucket"
        }):
            settings = Settings.from_environment()

            assert settings.aws_region == "ap-southeast-1"