from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float
    brand: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProductRead(ProductBase):
    id: int


class ProductCreate(ProductBase):
    pass