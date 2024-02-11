import os
import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timezone
print(os.getcwd())
from event_generation_sensors import main
from azure.storage.blob import BlobServiceClient

def mocked_uuid4():
    return "mocked-uuid"

def mocked_datetime_utcnow():
    return datetime(2024, 2, 11, 8, 55, 0, tzinfo=timezone.utc)

def mocked_random_choice(choices):
    return choices[0]

def mocked_random_uniform(a, b):
    return 0.5

@patch("uuid.uuid4", side_effect=mocked_uuid4)
@patch("datetime.datetime.utcnow", side_effect=mocked_datetime_utcnow)
@patch("random.choice", side_effect=mocked_random_choice)
@patch("random.uniform", side_effect=mocked_random_uniform)
class TestEventGenerationSensors(unittest.TestCase):

    def test_success(self, mock_random_uniform, mock_random_choice, mock_datetime, mock_uuid):
        os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "connection_string"
        os.environ["AZURE_STORAGE_CONTAINER_NAME"] = "container_name"
        os.environ["AZURE_STORAGE_ACCOUNT_NAME"] = "storage_account_name"

        with patch("azure.storage.blob.BlobServiceClient") as mock_blob_service_client:
            mock_blob_client = Mock()
            mock_blob_service_client.get_container_client.return_value.get_blob_client.return_value = mock_blob_client

            result = main(Mock())

            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.mimetype, "text/plain")
            self.assertIn("JSON file mocked-uuid.json generated and uploaded: https://storage_account_name.blob.core.windows.net/mocked-uuid.json", result.body)

            mock_blob_client.upload_blob.assert_called_once()

    def test_error(self, mock_random_uniform, mock_random_choice, mock_datetime, mock_uuid):
        with patch("os.environ.get", return_value=None):
            result = main(Mock())

            self.assertEqual(result.status_code, 500)
            self.assertEqual(result.mimetype, "text/plain")
            self.assertIn("Error generating and uploading JSON: Environment variable AZURE_STORAGE_CONNECTION_STRING not set", result.body)