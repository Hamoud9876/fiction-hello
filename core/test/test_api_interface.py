from core.src.api_interface import app
from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


class TestHealthcheck:
    def test_status_200(self, client):
        response = client.get("/healthcheck")

        assert response.status_code == 200


class TestCreateRecords:
    def test_status_400(self, client):
        response = client.get("/create_records?num_records=0")
        assert response.status_code == 400

    @patch("core.src.main.create_tables")
    @patch("core.src.main.insert_tables")
    def test_status_200(self, mock_insert, mock_create, client):
        response = client.get("/create_records?num_records=1")
        mock_insert.assert_called_once()
        mock_create.assert_called_once()
        assert response.status_code == 200

    @patch("core.src.main.create_tables")
    @patch("core.src.main.insert_tables")
    def test_contains_correct_body(self, mock_insert, mock_create, client):
        response = client.get("/create_records?num_records=1")
        assert response.json()["status"] == "Ok"
        assert response.json()["records_created"] == 1
        mock_insert.assert_called_once()
        mock_create.assert_called_once()

    @patch("core.src.main.create_tables")
    @patch("core.src.main.insert_tables")
    def test_create_multiple_records(self, mock_insert, mock_create, client):
        response = client.get("/create_records?num_records=20")
        assert response.json()["records_created"] == 20
        mock_insert.assert_called_once()
        mock_create.assert_called_once()

        response = client.get("/create_records?num_records=62")
        assert response.json()["records_created"] == 62
        assert mock_insert.call_count == 2
        assert mock_create.call_count == 2

        response = client.get("/create_records?num_records=144")
        assert response.json()["records_created"] == 144
        assert mock_insert.call_count == 3
        assert mock_create.call_count == 3
