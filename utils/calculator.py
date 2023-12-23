import os
from typing import List

import pandas as pd

from .config import RECIPE_URL
from .ingestion import get_ingestion_path, scrape_recipe
from .logger import logger
from .transformation import scale_quantity, separate_units


def load_default_recipe(unit_system, ignore_ingested_recipe):
    ingestion_path = get_ingestion_path(unit_system)
    if ignore_ingested_recipe or not os.path.exists(ingestion_path):
        logger.info(f"Scraping recipe from URL ({RECIPE_URL})...")
        scraped_recipe = scrape_recipe(RECIPE_URL, unit_system)
        if not scraped_recipe:
            logger.warning("Failed to scrape recipe. Empty recipe received.")
            return []
        logger.info(f"Successfully scraped recipe from URL ({RECIPE_URL}).")

    ingredients_df = pd.read_csv(ingestion_path).fillna("")
    return ingredients_df


def calculate_recipe(
    serving_size: int, unit_system: str, ignore_ingested_recipe=False
) -> List[str]:
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
