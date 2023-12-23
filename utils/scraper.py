from typing import List

import requests
from bs4 import BeautifulSoup

from .logger import logger


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
