from pydantic import BaseModel, ConfigDict, Field, computed_field
from typing import Optional

from app.core.models import Product
from app.schemas.product import ProductRead

class IngredientCreate(BaseModel):
    product_id: int
    weight_grams: float

    model_config = ConfigDict(from_attributes=True)

class IngredientRead(IngredientCreate):
    product: Optional[ProductRead] = None

class RecipeCreate(BaseModel):
    name: str
    instructions: Optional[str]
    ingredients: list[IngredientCreate] = Field(validation_alias="recipe_ingredients")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RecipeRead(BaseModel):
    id: int
    name: str
    instructions: Optional[str]
    ingredients: list[IngredientRead] = Field(validation_alias="recipe_ingredients")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @computed_field
    def total_calories(self) -> float:
        total = sum(
            (ing.product.calories / 100) * ing.weight_grams
            for ing in self.ingredients if ing.product
        )
        return round(total, 1)

    @computed_field
    def total_proteins(self) -> float:
        total = sum(
            (ing.product.proteins / 100) * ing.weight_grams
            for ing in self.ingredients if ing.product
        )
        return round(total, 1)

    @computed_field
    def total_fats(self) -> float:
        total = sum(
            (ing.product.fats / 100) * ing.weight_grams
            for ing in self.ingredients if ing.product
        )
        return round(total, 1)

    @computed_field
    def total_carbs(self) -> float:
        total = sum(
            (ing.product.carbs / 100) * ing.weight_grams
            for ing in self.ingredients if ing.product
        )
        return round(total, 1)


    @computed_field
    def calories_per_100g(self) -> float:

        total_weight = sum(ing.weight_grams for ing in self.ingredients)
        if total_weight == 0:
            return 0.0
        return round((self.total_calories / total_weight) * 100, 1)

    @computed_field
    def proteins_per_100g(self) -> float:

        total_weight = sum(ing.weight_grams for ing in self.ingredients)
        if total_weight == 0:
            return 0.0
        return round((self.total_proteins / total_weight) * 100, 1)

    @computed_field
    def fats_per_100g(self) -> float:

        total_weight = sum(ing.weight_grams for ing in self.ingredients)
        if total_weight == 0:
            return 0.0
        return round((self.total_fats / total_weight) * 100, 1)

    @computed_field
    def carbs_per_100g(self) -> float:

        total_weight = sum(ing.weight_grams for ing in self.ingredients)
        if total_weight == 0:
            return 0.0
        return round((self.total_carbs / total_weight) * 100, 1)