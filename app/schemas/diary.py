from datetime import date
from pydantic import BaseModel, ConfigDict, model_validator, Field, computed_field
from app.core.models.enums import MealType
from typing import Optional

from app.schemas.product import ProductRead


class DiaryEntryCreate(BaseModel):
    weight_grams: float
    meal_type: MealType
    date: date
    product_id: int | None = Field(default=None, gt=0)
    recipe_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def check_product_or_recipe(self):
        p_id = self.product_id
        r_id = self.recipe_id

        if p_id is None and r_id is None:
            raise ValueError("Нужно указать либо продукт, либо рецепт")
        if p_id is not None and r_id is not None:
            raise ValueError("Нельзя указать продукт и рецепт одновременно")

        return self


    model_config = ConfigDict(from_attributes=True)

class DiaryEntryRead(BaseModel):
    id: int
    date: date
    weight_grams: float
    meal_type: MealType
    product: Optional[ProductRead]

    @computed_field
    def total_proteins(self) -> float:
        if self.product:
            return round((self.product.proteins / 100) * self.weight_grams, 1)
        return 0.0

    @computed_field
    def total_fats(self) -> float:
        if self.product:
            return round((self.product.fats / 100) * self.weight_grams, 1)
        return 0.0

    @computed_field
    def total_carbs(self) -> float:
        if self.product:
            return round((self.product.carbs / 100) * self.weight_grams, 1)
        return 0.0

class DiaryEntryUpdate(BaseModel):
    date: Optional[date] = None
    weight_grams: float | None = None
    meal_type: MealType | None = None
    product_id: int | None = Field(default=None, gt=0)
    recipe_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def check_product_or_recipe(self):
        if self.product_id is not None and self.recipe_id is not None:
            raise ValueError("Нельзя указать продукт и рецепт одновременно")
        return self

