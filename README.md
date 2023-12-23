# Recipe Ingestion and Calculation Script

# Summary:

This codebase comprises a Recipe Calculator that scrapes a specific recipe (e.g., Carbonara) from a designated URL (https://www.cookingnook.com/recipe/carbonara/) and allows users to scale its serving size. The script provides functionality to ingest the recipe, perform calculations based on desired serving sizes and unit systems, and exposes FastAPI endpoints for triggering ingestion and calculations. Additionally, the codebase includes Docker configuration for easy deployment by containerizing the application.

## Setup:

1. Python Environment:
   - Ensure Python 3.x is installed.

2. Install Dependencies:
   - Run `pip install -r requirements/script.txt` to install required dependencies (`requests`, `beautifulsoup4`, `selenium`).

3. WebDriver Setup (for Selenium):
   - Install the appropriate WebDriver (e.g., ChromeDriver) and configure its path in the system environment variables.

4. Docker Setup (optional):
   - Ensure Docker is installed and running on your system.

## Script Usage:

### Command Line Arguments:

- `-ingestion`: Perform recipe ingestion.
- `--force_ingestion`: Force ingestion even if the ingestion path exists (default is `False`).
- `-calculate`: Perform recipe calculation.
- `--serving_size`: Specify desired serving size (default is `4`).
- `--unit_system`: Choose unit system ('US Customary' or 'Metric') for calculations (default is 'US Customary').
- `--ignore_ingested_recipe`: Ignore ingested recipe and scrape from scratch before calculation (default is `False`).

### Running the Script:

#### Ingestion:
- To scrape default recipe and save as CSVs for both unit systems (will skip if CSVs already exist):
    - `python script.py -ingestion`
- To force re-ingestion regardless if CSVs already exist or not:
    - `python script.py -ingestion --force_ingestion`

#### Recipe Calculation:
- To calculate recipe using default values (`serving_size=4` and `unit_system='US Customary'`):
    - `python script.py -calculate`
- To calculate recipe for different `serving_size`:
    - `python script.py -calculate --serving_size=1 --unit_system='US Customary'`
- To calculate recipe for different `serving_size` and `unit_system='Metric'`:
    - `python script.py -calculate --serving_size=1 --unit_system=Metric`
- By default, recipe is calculated using ingested CSVs, but can also ignore these and scrape from scratch:
    - `python script.py -calculate --serving_size=1 --unit_system=Metric --ignore_ingested_recipe`

## API Usage:

### FastAPI Endpoints:

- `/ingest_recipe`: GET endpoint to trigger recipe ingestion.
- `/calculate_recipe`: GET endpoint to calculate the recipe based on specified parameters.

### Docker:

- To build the Docker image:
  `docker build -t recipe-calculator .`
- To run the Docker container:
  `docker run -d -p 5000:5000 recipe-calculator`
- To view the FastAPI Swagger Docs, visit `http://127.0.0.1:5000/docs`

## Notes:

- For recipe calculations, ensure the WebDriver for Selenium is correctly installed and configured.
- The script offers flexibility in managing recipes and serving sizes through ingestion and calculation options.
