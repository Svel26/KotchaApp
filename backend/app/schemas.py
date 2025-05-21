# File: ah_collectibles_backend/app/schemas.py
from pydantic import BaseModel, Field # Make sure Field is imported

class CollectibleBase(BaseModel):
    name: str
    store_section: str
    # Use a "standard" Python attribute name and alias it to the JSON key with underscore
    model_3d_path: str = Field(alias="_3d_model_path") # CHANGED HERE
    riddle_hint: str
    product_information: str
    food_waste_tip: str
    nfc_tag_id: str

    model_config = { # UPDATED for Pydantic V2 style
        "from_attributes": True,  # Replaces orm_mode = True
        "populate_by_name": True  # Crucial for allowing population by alias
    }

class CollectibleCreate(CollectibleBase):
    character_id: int
    # model_config is inherited

class CollectibleResponse(CollectibleBase):
    character_id: int
    # model_config is inherited
    # Note: This response will now serialize with the key "model_3d_path".
    # If the API response *must* contain "_3d_model_path", we'd need to add:
    # model_3d_path: str = Field(alias="_3d_model_path", serialization_alias="_3d_model_path")
    # For now, we'll keep it simpler; the response key will be "model_3d_path".