# File: ah_collectibles_backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
import json
import os

def get_collectible(db: Session, character_id: int):
    return db.query(models.Collectible).filter(models.Collectible.character_id == character_id).first()

def get_collectibles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Collectible).offset(skip).limit(limit).all()

def create_collectible(db: Session, collectible: schemas.CollectibleCreate):
    db_collectible = models.Collectible(
        character_id=collectible.character_id,
        name=collectible.name,
        store_section=collectible.store_section,
        model_3d_path=collectible.model_3d_path,
        riddle_hint=collectible.riddle_hint,
        product_information=collectible.product_information,
        food_waste_tip=collectible.food_waste_tip,
        nfc_tag_id=collectible.nfc_tag_id
    )
    db.add(db_collectible)
    db.commit()
    db.refresh(db_collectible)
    return db_collectible

def populate_db_from_json(db: Session, json_file_path: str):
    if db.query(models.Collectible).first():
        print("Database already appears to be populated. Skipping population.")
        return

    if not os.path.exists(json_file_path):
        print(f"Error: JSON data file not found at {json_file_path}")
        print("Please run `python generate_initial_data.py` first from the project root.")
        return

    with open(json_file_path, 'r') as f:
        data = json.load(f)
        for item_data in data:
            collectible_schema = schemas.CollectibleCreate(**item_data)

            exists_by_id = db.query(models.Collectible).filter(models.Collectible.character_id == collectible_schema.character_id).first()
            exists_by_nfc = db.query(models.Collectible).filter(models.Collectible.nfc_tag_id == collectible_schema.nfc_tag_id).first()
            if not exists_by_id and not exists_by_nfc:
                 create_collectible(db=db, collectible=collectible_schema)
            else:
                print(f"Skipping already existing collectible: ID {collectible_schema.character_id} / NFC {collectible_schema.nfc_tag_id}")
    print(f"Database population attempt from {json_file_path} complete.")