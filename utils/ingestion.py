import os
from typing import List

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import selenium_options, RECIPE_URL, VALID_UNIT_SYSTEMS, INGESTION_PATH
from .logger import logger


def scrape_recipe(url: str, unit_system: str) -> List[str]:
    try:
        if unit_system == VALID_UNIT_SYSTEMS["us"]:
            logger.info(f"Scraping recipe for {VALID_UNIT_SYSTEMS['us']}...")
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            ingredients = soup.find("ul", class_="wprm-recipe-ingredients").find_all(
                "li"
            )
            ingredient_list = [ingredient.get_text() for ingredient in ingredients]
            return ingredient_list

        if unit_system == VALID_UNIT_SYSTEMS["metric"]:
            driver = webdriver.Chrome(options=selenium_options)
            driver.get(url)

            metric_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Metric']"))
            )
            metric_button.click()

            parent_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "wprm-recipe-ingredients")
                )
            )
            li_elements = parent_element.find_elements(
                By.CSS_SELECTOR, ".wprm-recipe-ingredient"
            )
            ingredient_list = [element.text for element in li_elements]
            return ingredient_list

    except requests.RequestException as e:
        logger.exception(f"Failed to fetch data from {url}: {e}")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        if "driver" in locals():
            driver.quit()

    return []


def ingest_recipe(force_ingestion=False, ingestion_path=INGESTION_PATH):
    path_exists = os.path.exists(ingestion_path)
    if path_exists and not force_ingestion:
        logger.info(f"The file path '{ingestion_path}' exists. Stopping ingestion.")
        return

    logger.info(
        f"The file path '{ingestion_path}' does not exist or force_ingestion flag is set. Proceeding with initial ingestion..."
    )

    us_recipe = scrape_recipe(RECIPE_URL, VALID_UNIT_SYSTEMS["us"])
    metric_recipe = scrape_recipe(RECIPE_URL, VALID_UNIT_SYSTEMS["metric"])

    df_recipe = pd.DataFrame(
        {
            VALID_UNIT_SYSTEMS["us"]: us_recipe,
            VALID_UNIT_SYSTEMS["metric"]: metric_recipe,
        }
    )
    df_recipe.to_csv(ingestion_path)
    logger.info(f"Successfully ingested default recipe to {ingestion_path}")