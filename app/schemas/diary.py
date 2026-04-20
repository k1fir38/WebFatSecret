from datetime import date
from pydantic import BaseModel, ConfigDict, model_validator, Field, computed_field

from app.core.calculators import calculate_macro_by_weight
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
        if not self.product: return 0.0
        return calculate_macro_by_weight(self.product.proteins, self.weight_grams)

    @computed_field
    def total_fats(self) -> float:
        if not self.product: return 0.0
        return calculate_macro_by_weight(self.product.fats, self.weight_grams)

    @computed_field
    def total_carbs(self) -> float:
        if not self.product: return 0.0
        return calculate_macro_by_weight(self.product.carbs, self.weight_grams)

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

class DiarySummary(BaseModel):
    date: date
    total_calories: float
    total_proteins: float
    total_fats: float
    total_carbs: float
    kcal_goal: float
    kcal_remaining: float
    kcal_overage: float
    goal_proteins: float
    goal_fats: float
    goal_carbs: float
    remaining_proteins: float
    remaining_fats: float
    remaining_carbs: float