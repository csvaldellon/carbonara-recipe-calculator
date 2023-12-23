import os
from typing import List

import pandas as pd

from .config import RECIPE_URL, INGESTION_PATH
from .logger import logger
from .transformation import scale_quantity, separate_units
from .ingestion import scrape_recipe


def load_default_recipe(unit_system, ignore_ingested_recipe):
    if ignore_ingested_recipe or not os.path.exists(INGESTION_PATH):
        logger.info(f"Scraping recipe from URL ({RECIPE_URL})...")
        scraped_recipe = scrape_recipe(RECIPE_URL, unit_system)
        if not scraped_recipe:
            logger.warning("Failed to scrape recipe. Empty recipe received.")
            return []
        logger.info(f"Successfully scraped recipe from URL ({RECIPE_URL}).")

    df_recipe = pd.read_csv(INGESTION_PATH)
    default_recipe = df_recipe[unit_system].tolist()
    return default_recipe


def calculate_recipe(
    serving_size: int, unit_system: str, ignore_ingested_recipe=False
) -> List[str]:
    try:
        default_recipe = load_default_recipe(unit_system, ignore_ingested_recipe)
        logger.info(
            f"Scaling quantities of ingredients based on serving size: {serving_size}..."
        )
        ingredients_df = separate_units(default_recipe)
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
