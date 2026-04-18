from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"  # Сидячий образ жизни
    LIGHT = "light"          # Легкие прогулки
    MODERATE = "moderate"    # Тренировки 3 раза в неделю
    INTENSE = "intense"      # Тяжелые нагрузки

class Goal(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    MAINTAIN = "maintain"
    GAIN_MUSCLE = "gain_muscle"

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class UnitName(str, Enum):
    GRAMS = "grams"
    PIECE = "piece"
    CUP = "cup"
    PORTION = "portion"