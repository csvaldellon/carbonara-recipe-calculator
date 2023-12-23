from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import selenium_options, VALID_UNIT_SYSTEMS
from .logger import logger


def scrape_recipe_in_us_scale(url: str) -> List[str]:
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
        logger.exception(f"Failed to fetch data from {url}: {e}")
        return []


def scrape_recipe_in_metric_scale(url: str) -> List[str]:
    driver = webdriver.Chrome(options=selenium_options)
    driver.get(url)

    try:
        metric_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Metric']"))
        )
        metric_button.click()

        parent_element = driver.find_element(By.CLASS_NAME, "wprm-recipe-ingredients")
        li_elements = parent_element.find_elements(
            By.CSS_SELECTOR, ".wprm-recipe-ingredient"
        )
        ingredient_list = [element.text for element in li_elements]

        return ingredient_list
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return []
    finally:
        driver.quit()


def scrape_recipe(url: str, unit_system: str) -> List[str]:
    if unit_system == VALID_UNIT_SYSTEMS["us"]:
        return scrape_recipe_in_us_scale(url)
    if unit_system == VALID_UNIT_SYSTEMS["metric"]:
        return scrape_recipe_in_metric_scale(url)
