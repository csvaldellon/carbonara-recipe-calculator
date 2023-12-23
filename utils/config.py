"""
Module for managing recipe data and scraping from a specified URL using Selenium.

Constants:
- RECIPE_URL (str): The URL of the recipe to scrape.
- INGESTION_PATH (str): Path to store the scraped default ingredients.
- DEFAULT_SERVING_SIZE (int): The default serving size for the recipe.
- VALID_UNIT_SYSTEMS (dict): Valid unit systems with their corresponding descriptions.

Selenium Options:
- selenium_options (selenium.webdriver.chrome.options.Options): Options for configuring Selenium WebDriver.
  - --no-sandbox: Disable the sandbox mode.
  - --disable-dev-shm-usage: Disable /dev/shm usage.
  - --headless: Run Chrome in headless mode (without a GUI).
"""

from selenium.webdriver.chrome.options import Options

RECIPE_URL = "https://www.cookingnook.com/recipe/carbonara/"
INGESTION_PATH = "./scraped_default_ingredients"
DEFAULT_SERVING_SIZE = 4
VALID_UNIT_SYSTEMS = {"us": "US Customary", "metric": "Metric"}

selenium_options = Options()
selenium_options.add_argument("--no-sandbox")
selenium_options.add_argument("--disable-dev-shm-usage")
selenium_options.add_argument("--headless")
