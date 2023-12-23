import re
from decimal import ROUND_HALF_UP, Decimal
from typing import List

import pandas as pd

from .config import DEFAULT_SERVING_SIZE


def separate_units(ingredients: List[str]) -> pd.DataFrame:
    """
    Splits the ingredients into quantities and ingredients.

    Steps:
    1. Parses each ingredient to separate its quantity and name.
    2. Creates a DataFrame with columns for quantity and ingredient.

    Args:
    - ingredients (List[str]): A list of ingredients.

    Returns:
    - pd.DataFrame: DataFrame containing columns 'quantity' and 'ingredient'.
    """

    def split_ingredient(ingredient):
        parts = re.split(r"(\d+\.?\d*\s*\-?\s*\d*\/?\d*)\s+(?=[^\d]+$)", ingredient)
        return (
            {"quantity": parts[-2].strip(), "ingredient": parts[-1].strip()}
            if len(parts) > 1
            else {"quantity": "", "ingredient": ingredient.strip()}
        )

    return pd.DataFrame([split_ingredient(ingredient) for ingredient in ingredients])


def round_and_scale(
    operand: float, quantity_multiplier: float, round_decimal_place: str = ".01"
):
    """
    Rounds the product of 'operand' multiplied by 'quantity_multiplier' to a specified decimal place.

    Args:
    - operand (float): The number to be multiplied.
    - quantity_multiplier (float): The value by which 'operand' is multiplied.
    - round_decimal_place (str, optional): The decimal place to which the result will be rounded. Defaults to ".01".

    Returns:
    - float: The result of 'operand' multiplied by 'quantity_multiplier', rounded to the specified decimal place.
    """
    scaled_operand = operand * quantity_multiplier
    return float(
        Decimal(scaled_operand).quantize(
            Decimal(round_decimal_place), rounding=ROUND_HALF_UP
        )
    )


def scale_quantity(
    quantity: str,
    serving_size: int,
    division_operation: str = "/",
    range_operation: str = " - ",
) -> str:
    """
    Scales the quantity of an ingredient based on the serving size.

    Steps:
    1. Checks the format of the quantity.
    2. Scales the quantity based on the serving size.

    Args:
    - quantity (str): The quantity of an ingredient.
    - serving_size (int): The desired serving size.
    - division_operation (str): Symbol for division in the quantity (default: "/").
    - range_operation (str): Symbol for a range of quantities (default: " - ").

    Returns:
    - str: Scaled quantity based on the serving size.

    Raises:
    - ValueError: If the quantity format is unexpected or cannot be parsed.
    """
    if not quantity:
        return ""

    if serving_size == DEFAULT_SERVING_SIZE:
        return quantity

    quantity_multiplier = serving_size / DEFAULT_SERVING_SIZE

    if division_operation in quantity:
        num, denom = map(float, quantity.split(division_operation))
        return str(round_and_scale(num / denom, quantity_multiplier))

    if range_operation in quantity:
        from_qty, to_qty = map(float, quantity.split(range_operation))
        return f"{round_and_scale(from_qty, quantity_multiplier)} - {round_and_scale(to_qty, quantity_multiplier)}"

    return str(round_and_scale(float(quantity), quantity_multiplier))
