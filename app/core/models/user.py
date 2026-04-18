
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, DATE
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from .base import Base
from .enums import Gender, ActivityLevel, Goal

if TYPE_CHECKING:
    from .diary import DiaryEntry
    from .product import Product
    from .recipe import Recipe
    from .weight_history import WeightHistory



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    gender: Mapped[Gender] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(DATE, nullable=False)

    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    activity_level: Mapped[ActivityLevel] = mapped_column(
        String, nullable=False,
        default=ActivityLevel.LIGHT
    )
    goal: Mapped[Goal] = mapped_column(
        String, nullable=False, default=Goal.MAINTAIN
    )

    # 1. Связь с дневником
    diary_entries: Mapped[list["DiaryEntry"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"  # Если удалить юзера, удалятся и его записи
    )

    # 2. Связь с историей веса
    weight_history: Mapped[list["WeightHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # 3. Связь с созданными продуктами
    custom_products: Mapped[list["Product"]] = relationship(
        back_populates="creator",
        foreign_keys="[Product.creator_id]"
    )

    # 4. Связь с рецептами
    recipes: Mapped[list["Recipe"]] = relationship(
        back_populates="creator"
    )

