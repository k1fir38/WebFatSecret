
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

    @property
    def calories_goal(self) -> float:
        today = date.today()
        birth = self.birth_date
        
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        # Для мужчин: (10 × вес) + (6.25 × рост) - (5 × возраст) + 5
        # Для женщин: (10 × вес) + (6.25 × рост) - (5 × возраст) - 161
        if self.gender == Gender.FEMALE:
            BMR = (10 * self.weight) + (6.25 * self.height) - (5 * age) - 161
        else:
            BMR = (10 * self.weight) + (6.25 * self.height) - (5 * age) + 5

        if  self.activity_level == ActivityLevel.SEDENTARY: BMR *= 1.2
        elif self.activity_level == ActivityLevel.LIGHT: BMR *= 1.375
        elif self.activity_level == ActivityLevel.MODERATE: BMR *= 1.55
        elif self.activity_level == ActivityLevel.INTENSE: BMR *= 1.725

        if self.goal == Goal.LOSE_WEIGHT: BMR *= 0.85
        elif self.goal == Goal.GAIN_MUSCLE: BMR *= 1.15

        return round(BMR)

    @property
    def proteins_goal(self) -> float:
        ratios = {
            Goal.LOSE_WEIGHT: 0.30,
            Goal.MAINTAIN: 0.20,
            Goal.GAIN_MUSCLE: 0.25
        }
        ratio = ratios.get(self.goal, 0.20)

        return round((self.calories_goal * ratio) / 4)

    @property
    def carbs_goal(self) -> float:
        ratios = {
            Goal.LOSE_WEIGHT: 0.40,
            Goal.MAINTAIN: 0.50,
            Goal.GAIN_MUSCLE: 0.50
        }
        ratio = ratios.get(self.goal, 0.50)

        return round((self.calories_goal * ratio) / 4)

    @property
    def fats_goal(self) -> float:
        ratios = {
            Goal.LOSE_WEIGHT: 0.30,
            Goal.MAINTAIN: 0.30,
            Goal.GAIN_MUSCLE: 0.25
        }
        ratio = ratios.get(self.goal, 0.30)

        return round((self.calories_goal * ratio) / 9)