# Recipe Ingestion and Calculation Script

## Setup:

1. Python Environment:
   - Ensure Python 3.x is installed.

2. Install Dependencies:
   - Run `pip install -r requirements.txt` to install required dependencies (`requests`, `beautifulsoup4`, `selenium`).

3. WebDriver Setup (for Selenium):
   - Install the appropriate WebDriver (e.g., ChromeDriver) and configure its path in the system environment variables.

## Usage:

### Command Line Arguments:

- `-ingestion`: Perform recipe ingestion.
- `--force_ingestion`: Force ingestion even if the ingestion path exists.
- `-calculate`: Perform recipe calculation.
- `--serving_size`: Specify desired serving size.
- `--unit_system`: Choose unit system ('us' or 'metric') for calculations.
- `--ignore_ingested_recipe`: Ignore ingested recipe and scrape from scratch before calculation.

### Running the Script:

#### Ingestion:
`python script_name.py -ingestion`

#### Recipe Calculation:
`python script_name.py -calculate --serving_size 4 --unit_system us`

## Notes:

- For recipe calculations, ensure the WebDriver for Selenium is correctly installed and configured.
- The script offers flexibility in managing recipes and serving sizes through ingestion and calculation options.
