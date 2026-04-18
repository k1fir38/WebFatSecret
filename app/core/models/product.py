

from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Float, DATE, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from .base import Base
from .enums import Gender, ActivityLevel, Goal, UnitName

if TYPE_CHECKING:
    from .user import User
    from .diary import DiaryEntry
    from .recipe import RecipeIngredient



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    proteins: Mapped[float] = mapped_column(Float, nullable=False)
    fats: Mapped[float] = mapped_column(Float, nullable=False)
    carbs: Mapped[float] = mapped_column(Float, nullable=False)

    creator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    creator: Mapped["User"] = relationship(back_populates="custom_products")
    units: Mapped[list["ProductUnit"]] = relationship(back_populates="product_units")
    diary: Mapped[list["DiaryEntry"]] = relationship(back_populates="product")
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(back_populates="product")


class ProductUnit(Base):
    __tablename__ = "product_units"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    unit_name: Mapped[UnitName] = mapped_column(
        String, nullable=False,
        default=UnitName.GRAMS
    )
    weight_grams: Mapped[float] = mapped_column(Float,nullable=False)

    product_units: Mapped[Product] = relationship(back_populates="units")