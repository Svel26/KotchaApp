from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Albert Heijn Collectibles API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        # This check prevents re-populating the DB every time you restart the server
        if crud.get_collectibles(db, skip=0, limit=1) == []:
            print("Database is empty, populating from JSON...")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(current_dir, "data", "collectibles_data.json")
            crud.populate_db_from_json(db, json_file_path)
        else:
            print("Database already contains data.")
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

@app.get("/collectibles/nfc/{nfc_tag_id}", response_model=schemas.CollectibleResponse)
def read_collectible_by_nfc_id(nfc_tag_id: str, db: Session = Depends(get_db)):
    db_collectible = crud.get_collectible_by_nfc_id(db, nfc_tag_id=nfc_tag_id)
    if db_collectible is None:
        raise HTTPException(status_code=404, detail="NFC Tag not found in database")
    return db_collectible

@app.post("/api/unlock-character", response_model=schemas.CollectibleResponse)
def unlock_character(unlock_request: schemas.UnlockRequest, db: Session = Depends(get_db)):
    db_collectible = crud.unlock_collectible_by_nfc_id(db, nfc_tag_id=unlock_request.serialNumber)
    if db_collectible is None:
        raise HTTPException(status_code=404, detail="NFC Tag not found")
    return db_collectible
