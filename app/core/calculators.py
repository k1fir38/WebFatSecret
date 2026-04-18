

def calculate_macro_by_weight(value_per_100g: float, weight_grams: float) -> float:
    """Универсальная формула расчета нутриента на заданный вес."""
    return round((value_per_100g / 100) * weight_grams, 1)