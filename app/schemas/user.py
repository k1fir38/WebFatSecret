from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from app.core.models.enums import Gender, ActivityLevel, Goal

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    gender: Gender
    birth_date: date
    weight: float
    height: float
    activity_level: ActivityLevel = ActivityLevel.LIGHT
    goal: Goal = Goal.MAINTAIN

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    calories_goal: float
    proteins_goal: float
    fats_goal: float
    carbs_goal: float

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    name: str | None = None
    gender: Gender | None = None
    birth_date: date | None = None
    weight: float | None = None
    height: float | None = None
    activity_level: ActivityLevel | None =  None
    goal: Goal | None  = None