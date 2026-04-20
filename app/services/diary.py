from datetime import date

from app.core.models.user import User
from app.core.models.diary import DiaryEntry

def get_daily_summary(entries_diary: list[DiaryEntry], user: User, diary_date: date):

    total_kcal = sum(item.calories_total for item in entries_diary)
    total_proteins = sum(item.proteins_total for item in entries_diary)
    total_fats = sum(item.fats_total for item in entries_diary)
    total_carbs = sum(item.carbs_total for item in entries_diary)

    diff = user.calories_goal - total_kcal

    if diff >= 0:
        kcal_remaining = round(diff, 1)
        kcal_overage = 0.0
    else:
        kcal_remaining = 0.0
        kcal_overage = round(abs(diff), 1)  # abs() превратит -500 в 500

    return {
        "date": diary_date,
        "total_calories": round(total_kcal, 1),
        "total_proteins": round(total_proteins, 1),
        "total_fats": round(total_fats, 1),
        "total_carbs": round(total_carbs, 1),

        "kcal_goal": user.calories_goal,
        "kcal_remaining": round(kcal_remaining, 1),
        "kcal_overage": round(kcal_overage, 1),

        "goal_proteins": user.proteins_goal,
        "goal_fats": user.fats_goal,
        "goal_carbs": user.carbs_goal,

        # Считаем остатки БЖУ
        "remaining_proteins": round(max(0, user.proteins_goal - total_proteins), 1),
        "remaining_fats": round(max(0, user.fats_goal - total_fats), 1),
        "remaining_carbs": round(max(0, user.carbs_goal - total_carbs), 1),
    }