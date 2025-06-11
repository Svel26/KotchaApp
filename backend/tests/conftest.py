import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import os

# Adjust relative path to go up one level from 'tests' then into 'app'
# This is crucial for Python to find the 'app' module correctly when pytest runs from the root.
# By adding the parent of 'backend' (which is the project root) to sys.path,
# we can then import 'backend.app.models' etc.
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


from backend.app.database import Base, get_db
from backend.app.models import Collectible as CollectibleModel
from backend.app.schemas import CollectibleCreate
from backend.app.main import app # Import the FastAPI app instance

# In-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Ensure same connection for in-memory DB
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Test data
LOCKED_NFC_ID = "test_nfc_locked_123"
UNLOCKED_NFC_ID = "test_nfc_unlocked_456"

TEST_COLLECTIBLES_DATA = [
    {
        "character_id": 101,
        "name": "Test Locked Character",
        "store_section": "Test Section",
        "model_3d_path": "path/to/model1.glb",
        "riddle_hint": "Locked hint",
        "product_information": "Locked info",
        "food_waste_tip": "Locked tip",
        "nfc_tag_id": LOCKED_NFC_ID,
        "is_unlocked": False, # Explicitly locked
    },
    {
        "character_id": 102,
        "name": "Test Unlocked Character",
        "store_section": "Test Section",
        "model_3d_path": "path/to/model2.glb",
        "riddle_hint": "Unlocked hint",
        "product_information": "Unlocked info",
        "food_waste_tip": "Unlocked tip",
        "nfc_tag_id": UNLOCKED_NFC_ID,
        "is_unlocked": True, # Explicitly unlocked
    },
]

@pytest.fixture(scope="function") # Changed to function scope for cleaner tests
def db_session():
    # Ensure models are loaded onto Base before create_all is called.
    # This is usually handled by top-level imports, but as an extra precaution:
    import backend.app.models

    """
    Fixture to provide a test database session.
    Creates all tables, populates initial data, yields session, then drops all tables.
    """
    Base.metadata.create_all(bind=test_engine) # Create tables
    db = TestingSessionLocal()
    try:
        # Populate with test data
        for item_data in TEST_COLLECTIBLES_DATA:
            # Need to handle is_unlocked separately if CollectibleCreate doesn't have it
            collectible_create_data = {k: v for k, v in item_data.items() if k != "is_unlocked"}
            db_collectible = CollectibleModel(
                **collectible_create_data,
                is_unlocked=item_data["is_unlocked"]
            )
            db.add(db_collectible)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine) # Drop tables after test

@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Fixture to provide a TestClient with overridden DB dependency
    and disabled startup events.
    """
    # Disable startup event for tests to prevent it from using prod DB or interfering
    original_startup_events = app.router.on_startup
    app.router.on_startup = []

    def override_get_db():
        try:
            yield db_session
        finally:
            # db_session is managed by its own fixture now
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client

    # Clean up
    app.dependency_overrides.clear()
    app.router.on_startup = original_startup_events # Restore startup events
