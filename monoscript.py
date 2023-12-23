import re
import logging
import argparse
from typing import List

import requests
import pandas as pd
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RECIPE_URL = "https://www.cookingnook.com/recipe/carbonara/"
DEFAULT_SERVING_SIZE = 4


def scrape_recipe(url: str) -> List[str]:
    """
    Fetches and extracts the ingredients list from the specified URL.

    Steps:
    1. Retrieves the webpage content from the provided URL.
    2. Parses the HTML content to extract the list of ingredients.

    Args:
    - url (str): The URL of the recipe page.

    Returns:
    - List[str]: A list of ingredients extracted from the URL.

    Raises:
    - requests.RequestException: If there's an issue with fetching the data from the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        ingredients = soup.find("ul", class_="wprm-recipe-ingredients").find_all("li")
        ingredient_list = [ingredient.get_text() for ingredient in ingredients]
        return ingredient_list
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        return []


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


def scale_quantity(
    quantity: str,
    serving_size: int,
    division_operation: str = "/",
    range_operation: str = " - ",
    round_decimal_units: int = 2,
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
    - round_decimal_units (int): Decimal places to round to (default: 2).

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
        return str(round((num / denom) * quantity_multiplier, round_decimal_units))

    if range_operation in quantity:
        from_qty, to_qty = map(float, quantity.split(range_operation))
        return f"{round(from_qty * quantity_multiplier, round_decimal_units)} - {round(to_qty * quantity_multiplier, round_decimal_units)}"

    return str(round(float(quantity) * quantity_multiplier, round_decimal_units))


def calculate_recipe(serving_size: int) -> List[str]:
    """
    Orchestrates the scraping, scaling, and formatting of the recipe.

    Steps:
    1. Scrapes the recipe ingredients.
    2. Separates quantities from ingredients.
    3. Scales ingredient quantities based on the serving size.
    4. Formats the ingredients into a list of strings.

    Args:
    - serving_size (int): The desired serving size for the recipe.

    Returns:
    - List[str]: A list of strings representing the ingredients for the adjusted serving size.

    Raises:
    - Exception: If there's an issue with the calculation process.
    """
    try:
        logger.info(f"Scraping recipe from URL ({RECIPE_URL})...")
        scraped_recipe = scrape_recipe(RECIPE_URL)
        if not scraped_recipe:
            logger.warning("Failed to scrape recipe. Empty recipe received.")
            return []
        logger.info(f"Successfully scraped recipe from URL ({RECIPE_URL}).")

        logger.info(
            f"Scaling quantities of ingredients based on serving size: {serving_size}..."
        )
        ingredients_df = separate_units(scraped_recipe)
        ingredients_df["scaled_quantity"] = ingredients_df["quantity"].apply(
            lambda x: scale_quantity(x, serving_size)
        )
        ingredients_df["recipe_line"] = (
            ingredients_df["scaled_quantity"] + " " + ingredients_df["ingredient"]
        )
        ingredients_df["recipe_line"] = ingredients_df["recipe_line"].str.strip()
        logger.info(
            f"Successfully scaled quantities of ingredients based on serving size: {serving_size}."
        )

        return ingredients_df["recipe_line"].tolist()
    except Exception as e:
        logger.exception(f"Failed to calculate recipe: {e}")
        return []


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Recipe Calculator")
    parser.add_argument(
        "--serving_size",
        type=float,
        default=DEFAULT_SERVING_SIZE,
        help="Desired serving size for the recipe (default: 4)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    serving_size = args.serving_size
    recipe = calculate_recipe(serving_size)
    if recipe:
        for line in recipe:
            print(line)
    else:
        print("Recipe calculation failed.")
