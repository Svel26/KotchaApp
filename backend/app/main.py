from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Albert Heijn Collectibles API")

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
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