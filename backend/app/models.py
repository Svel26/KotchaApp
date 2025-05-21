# File: ah_collectibles_backend/app/models.py
from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Collectible(Base):
    __tablename__ = "collectibles"

    character_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    store_section = Column(String)
    model_3d_path = Column(String) # CHANGED HERE (was _3d_model_path)
    riddle_hint = Column(Text)
    product_information = Column(Text)
    food_waste_tip = Column(Text)
    nfc_tag_id = Column(String, unique=True, index=True)