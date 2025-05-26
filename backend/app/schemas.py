from pydantic import BaseModel, Field

class CollectibleBase(BaseModel):
    name: str
    store_section: str
    model_3d_path: str = Field(alias="_3d_model_path")
    riddle_hint: str
    product_information: str
    food_waste_tip: str
    nfc_tag_id: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class CollectibleCreate(CollectibleBase):
    character_id: int

class CollectibleResponse(CollectibleBase):
    character_id: int