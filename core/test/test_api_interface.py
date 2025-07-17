from core.src.api_interface import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="function")
def client():
    return TestClient(app)

class TestHealthcheck:
    def test_status_200(self,client):
        response = client.get("/healthcheck")

        assert response.status_code == 200

class TestCreateRecords:
    def test_status_400(slef, client):
        response = client.get("/create_records?num_records=0")
        assert response.status_code == 400

    def test_status_200(self,client):
        response = client.get("/create_records?num_records=1")
        assert response.status_code == 200

    def test_contains_correct_body(slef,client):
        response = client.get("/create_records?num_records=1")
        assert response.json()["status"] == "Ok"
        assert response.json()["records_created"] == 1

    def test_create_multiple_records(self, client):
        response = client.get("/create_records?num_records=20")
        assert response.json()["records_created"] == 20

        response = client.get("/create_records?num_records=62")
        assert response.json()["records_created"] == 62

        response = client.get("/create_records?num_records=144")
        assert response.json()["records_created"] == 144

