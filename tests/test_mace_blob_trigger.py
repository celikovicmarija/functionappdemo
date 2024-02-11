import logging
import json
import os
from unittest.mock import patch
import pytest

from psycopg2 import connect, sql

from azure.functions import Function, InputStream

from mace_blob_trigger import main  # Import the function to test

# Mock external dependencies
@pytest.fixture
def mock_env_vars():
    with patch.dict("os.environ", {"host": "mock_host", "user": "mock_user", "password": "mock_password"}):
        yield

@pytest.fixture
def mock_psycopg2():
    with patch("psycopg2.connect") as mock_connect:
        yield mock_connect

# Test cases with mocks
def test_main_successful_insertion(mock_env_vars, mock_psycopg2):
    mock_blob = InputStream(b'{"timestamp": 1668054617, "module": "A", "sensor_id": 1, "sensor_type": "temperature", "value": 25.5, "unit": "C"}')
    main(mock_blob)

    mock_psycopg2.assert_called_once_with(
        host="mock_host",
        database="postgres",
        user="mock_user",
        password="mock_password",
    )
    mock_psycopg2().cursor().execute.assert_called_once_with(
        sql.SQL(
            """
            INSERT INTO public.station_data (timestamp, module, sensor_id, sensor_type, value, unit)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        ),
        (1668054617, "A", 1, "temperature", 25.5, "C"),
    )
    mock_psycopg2().commit.assert_called_once()

# Additional test cases
def test_main_handles_invalid_json_data(mock_env_vars):
    mock_blob = InputStream(b'{"invalid_json")')
    with pytest.raises(json.JSONDecodeError):
        main(mock_blob)