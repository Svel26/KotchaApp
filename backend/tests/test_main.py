import pytest
from fastapi.testclient import TestClient

# conftest.py should be in the same directory or an ancestor directory
# for these fixtures to be automatically discovered by pytest.
# No explicit import of fixtures is needed if conftest is set up correctly.

# From conftest.py, we expect:
# - test_client: a TestClient instance with DB override
# We will also use constants defined in conftest.py
from backend.tests.conftest import LOCKED_NFC_ID, UNLOCKED_NFC_ID # Import test constants

def test_unlock_locked_character(test_client: TestClient):
    """Test unlocking a character that is currently locked."""
    response = test_client.post(
        "/api/unlock-character",
        json={"serialNumber": LOCKED_NFC_ID}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_unlocked"] is True
    assert data["nfc_tag_id"] == LOCKED_NFC_ID
    assert data["name"] == "Test Locked Character" # Check other data too

def test_unlock_non_existent_nfc_id(test_client: TestClient):
    """Test attempting to unlock with an NFC ID that does not exist."""
    response = test_client.post(
        "/api/unlock-character",
        json={"serialNumber": "non_existent_nfc_id_123"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "NFC Tag not found"

def test_unlock_already_unlocked_character(test_client: TestClient):
    """Test attempting to unlock a character that is already unlocked."""
    response = test_client.post(
        "/api/unlock-character",
        json={"serialNumber": UNLOCKED_NFC_ID}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_unlocked"] is True
    assert data["nfc_tag_id"] == UNLOCKED_NFC_ID
    assert data["name"] == "Test Unlocked Character"

def test_unlock_invalid_request_body_missing_serial(test_client: TestClient):
    """Test unlock attempt with a request body missing the serialNumber field."""
    response = test_client.post(
        "/api/unlock-character",
        json={} # Missing serialNumber
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error

def test_unlock_invalid_request_body_wrong_type(test_client: TestClient):
    """Test unlock attempt with a request body with wrong type for serialNumber."""
    response = test_client.post(
        "/api/unlock-character",
        json={"serialNumber": 12345} # serialNumber should be a string
    )
    assert response.status_code == 422 # Unprocessable Entity
    # You could also check the error details if needed:
    # data = response.json()
    # assert "Input should be a valid string" in str(data["detail"])

# Example of checking the database state directly (optional, but good for complex tests)
# This requires the db_session fixture to be passed to the test function.
def test_unlock_locked_character_db_check(test_client: TestClient, db_session):
    """
    Test unlocking a locked character and verify the change in the database.
    This test requires the db_session fixture from conftest.py.
    """
    from backend.app.models import Collectible as CollectibleModel

    # Initial state check (optional, could be assumed from conftest)
    initial_collectible = db_session.query(CollectibleModel).filter(CollectibleModel.nfc_tag_id == LOCKED_NFC_ID).first()
    assert initial_collectible is not None
    assert initial_collectible.is_unlocked is False

    response = test_client.post(
        "/api/unlock-character",
        json={"serialNumber": LOCKED_NFC_ID}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_unlocked"] is True

    # Verify in DB
    db_session.commit() # Ensure session sees changes made by test_client if transactions are tricky
    unlocked_collectible = db_session.query(CollectibleModel).filter(CollectibleModel.nfc_tag_id == LOCKED_NFC_ID).first()
    assert unlocked_collectible is not None
    assert unlocked_collectible.is_unlocked is True
