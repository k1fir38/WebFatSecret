from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Float, DATE, ForeignKey, Text, Null
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from .base import Base
from .enums import UnitName

if TYPE_CHECKING:
    from .user import User
    from .diary import DiaryEntry
    from .product import Product



class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=Null)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="recipes")
    diary: Mapped["DiaryEntry"] = relationship(back_populates="recipe")
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(back_populates="recipe")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    weight_grams: Mapped[float] = mapped_column(Float, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="recipe_ingredients")
    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")