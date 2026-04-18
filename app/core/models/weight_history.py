from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, DATE, ForeignKey, Text, Null
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from .base import Base
from .enums import MealType

if TYPE_CHECKING:
    from .user import User



class WeightHistory(Base):
    __tablename__ = "weight_histories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[date] = mapped_column(DATE, nullable=False, index=True)
    weight_kilograms: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped["User"] = relationship(back_populates="weight_history")