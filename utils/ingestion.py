import os
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .config import INGESTION_PATH, RECIPE_URL, VALID_UNIT_SYSTEMS, selenium_options
from .logger import logger
from .transformation import separate_units


def scrape_us_recipe(url: str) -> List[str]:
    """
    Scrape the recipe using US customary units.

    Args:
    - url (str): The URL of the recipe to scrape.

    Returns:
    List[str]: List of ingredients for the recipe.
    """
    try:
        logger.info(f"Scraping recipe for {VALID_UNIT_SYSTEMS['us']}...")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        ingredients = soup.find("ul", class_="wprm-recipe-ingredients").find_all("li")
        return [ingredient.get_text() for ingredient in ingredients]
    except requests.RequestException as e:
        logger.exception(f"Failed to fetch data from {url}: {e}")
        return []
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return []


def scrape_metric_recipe(driver: webdriver.Chrome, url: str) -> List[str]:
    """
    Scrape the recipe using metric units.

    Args:
    - driver (webdriver.Chrome): The Chrome WebDriver instance.
    - url (str): The URL of the recipe to scrape.

    Returns:
    List[str]: List of ingredients for the recipe.
    """
    try:
        logger.info(f"Scraping recipe for {VALID_UNIT_SYSTEMS['metric']}...")
        driver.get(url)
        metric_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Metric']"))
        )
        metric_button.click()
        parent_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wprm-recipe-ingredients"))
        )
        li_elements = parent_element.find_elements(
            By.CSS_SELECTOR, ".wprm-recipe-ingredient"
        )
        return [element.text for element in li_elements]
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return []


def scrape_recipe(url: str, unit_system: str) -> List[str]:
    """
    Scrape the recipe based on the specified unit system.

    Args:
    - url (str): The URL of the recipe to scrape.
    - unit_system (str): The unit system for scraping.

    Returns:
    List[str]: List of ingredients for the recipe.
    """
    if unit_system == VALID_UNIT_SYSTEMS["us"]:
        return scrape_us_recipe(url)
    elif unit_system == VALID_UNIT_SYSTEMS["metric"]:
        try:
            with webdriver.Chrome(options=selenium_options) as driver:
                return scrape_metric_recipe(driver, url)
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return []
    else:
        logger.warning(f"Unsupported unit system: {unit_system}")
        return []


def get_ingestion_path(unit_system):
    """
    Get the ingestion path based on the unit system.

    Args:
    - unit_system: The unit system for the ingestion path.

    Returns:
    str: The ingestion path.
    """
    return INGESTION_PATH + "_" + unit_system.lower().replace(" ", "_") + ".csv"


def ingest_recipe(force_ingestion=False):
    """
    Ingest the recipe data into CSV files based on unit systems.

    Args:
    - force_ingestion (bool, optional): Flag to force data ingestion if paths exist.

    Returns:
    None
    """
    for unit_system in VALID_UNIT_SYSTEMS.values():
        ingestion_path = get_ingestion_path(unit_system)
        path_exists = os.path.exists(ingestion_path)

        if path_exists and not force_ingestion:
            logger.info(f"The file path '{ingestion_path}' exists. Stopping ingestion.")
        else:
            logger.info(
                f"The file path '{ingestion_path}' does not exist or force_ingestion flag is set. Proceeding with initial ingestion..."
            )
            scraped_recipe = scrape_recipe(RECIPE_URL, unit_system)
            df_ingredients = separate_units(scraped_recipe)
            df_ingredients.to_csv(ingestion_path)
            logger.info(f"Successfully ingested default recipe to {ingestion_path}")
