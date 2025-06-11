from sqlalchemy import Column, Integer, String, Text, Boolean
from .database import Base

class Collectible(Base):
    __tablename__ = "collectibles"

    character_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    store_section = Column(String)
    model_3d_path = Column(String)
    riddle_hint = Column(Text)
    product_information = Column(Text)
    food_waste_tip = Column(Text)
    nfc_tag_id = Column(String, unique=True, index=True)
    is_unlocked = Column(Boolean, default=False)