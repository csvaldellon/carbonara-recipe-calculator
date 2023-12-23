from selenium.webdriver.chrome.options import Options

RECIPE_URL = "https://www.cookingnook.com/recipe/carbonara/"
DEFAULT_SERVING_SIZE = 4
VALID_UNIT_SYSTEMS = {"us": "US Customary", "metric": "Metric"}

selenium_options = Options()
selenium_options.add_argument("--no-sandbox")
selenium_options.add_argument("--disable-dev-shm-usage")
selenium_options.add_argument("--headless")
