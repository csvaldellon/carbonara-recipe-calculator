from typing import List

from .config import RECIPE_URL
from .logger import logger
from .scaler import scale_quantity, separate_units
from .scraper import scrape_recipe


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
