from typing import List
import argparse

from utils.scraper import scrape_recipe
from utils.scaler import (
    separate_units,
    scale_quantity
)
from config import (
    RECIPE_URL,
    DEFAULT_SERVING_SIZE
)
from logger import logger


def calculate_recipe(
    serving_size: int
) -> List[str]:
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
        scraped_recipe = scrape_recipe(RECIPE_URL)
        if not scraped_recipe:
            logger.warning("Failed to scrape recipe. Empty recipe received.")
            return []

        ingredients_df = separate_units(scraped_recipe)
        ingredients_df['scaled_quantity'] = ingredients_df['quantity'].apply(lambda x: scale_quantity(x, serving_size))
        ingredients_df['recipe_line'] = ingredients_df['scaled_quantity'] + ' ' + ingredients_df['ingredient']
        ingredients_df['recipe_line'] = ingredients_df['recipe_line'].str.strip()

        return ingredients_df['recipe_line'].tolist()
    except Exception as e:
        logger.exception(f"Failed to calculate recipe: {e}")
        return []


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Recipe Calculator')
    parser.add_argument('--serving_size', type=int, default=DEFAULT_SERVING_SIZE,
                        help='Desired serving size for the recipe (default: 4)')

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