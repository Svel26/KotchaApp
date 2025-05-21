from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os # For path joining

# Ensure correct relative imports for modules within the 'app' package
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# Create all tables in the database
# This should ideally be managed by Alembic for migrations in a larger app
# It's safe to call this multiple times; it only creates tables that don't exist.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Albert Heijn Collectibles API")

# Dependency to populate DB on first startup (for demo purposes)
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        # Construct the path to the JSON file relative to this main.py file
        # Assumes main.py is in 'app/' and data is in 'app/data/'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, "data", "collectibles_data.json")
        crud.populate_db_from_json(db, json_file_path)
    finally:
        db.close()

@app.get("/collectibles/", response_model=List[schemas.CollectibleResponse])
def read_collectibles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    collectibles = crud.get_collectibles(db, skip=skip, limit=limit)
    return collectibles

@app.get("/collectibles/{character_id}", response_model=schemas.CollectibleResponse)
def read_collectible(character_id: int, db: Session = Depends(get_db)):
    db_collectible = crud.get_collectible(db, character_id=character_id)
    if db_collectible is None:
        raise HTTPException(status_code=404, detail="Collectible not found")
    return db_collectible

# To run the app (from the `ah_collectibles_backend` directory):
# 1. Ensure you have a virtual environment set up and activated.
# 2. Install requirements: pip install -r requirements.txt
# 3. Generate initial data: python generate_initial_data.py
# 4. Run uvicorn: uvicorn app.main:app --reload
#
# Then access http://127.0.0.1:8000/docs in your browser.