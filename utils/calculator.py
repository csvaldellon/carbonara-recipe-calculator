import os
from typing import List

import pandas as pd

from .config import RECIPE_URL
from .ingestion import get_ingestion_path, scrape_recipe
from .logger import logger
from .transformation import scale_quantity


def load_default_recipe(unit_system: str, ignore_ingested_recipe: bool) -> pd.DataFrame:
    """
    Loads the default recipe either from a stored file or by scraping from URL.

    Args:
    - unit_system (str): The unit system to determine the recipe format.
    - ignore_ingested_recipe (bool): Flag to ignore the stored recipe file.

    Returns:
    pd.DataFrame: DataFrame containing the loaded recipe.
    """
    ingestion_path = get_ingestion_path(unit_system)

    if ignore_ingested_recipe or not os.path.exists(ingestion_path):
        logger.info(f"Scraping recipe from URL ({RECIPE_URL})...")
        scraped_recipe = scrape_recipe(RECIPE_URL, unit_system)

        if not scraped_recipe:
            logger.warning("Failed to scrape recipe. Received an empty recipe.")
            return pd.DataFrame()

        logger.info(f"Successfully scraped recipe from URL ({RECIPE_URL}).")

    return pd.read_csv(ingestion_path).fillna("")


def calculate_recipe(
    serving_size: int, unit_system: str, ignore_ingested_recipe: bool = False
) -> List[str]:
    """
    Calculates the recipe based on the serving size by scaling ingredient quantities.

    Args:
    - serving_size (int): The desired serving size for the recipe.
    - unit_system (str): The unit system used for the recipe.
    - ignore_ingested_recipe (bool): Flag to ignore the stored recipe file.

    Returns:
    List[str]: List of strings representing the calculated recipe lines.
    """
    try:
        logger.info(
            f"Scaling quantities of ingredients based on serving size: {serving_size}..."
        )
        ingredients_df = load_default_recipe(unit_system, ignore_ingested_recipe)

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
