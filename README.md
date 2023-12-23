# carbonara-recipe-calculator

# Recipe Calculator

This Python script scrapes a recipe from a specified URL and adjusts the ingredient quantities based on a desired serving size.

## Features

- **Scraping**: Fetches the ingredients list from a provided recipe URL.
- **Scaling**: Adjusts ingredient quantities based on the desired serving size.
- **Formatting**: Presents the ingredients list for the adjusted serving size.

## Requirements

- Python 3.x
- Libraries: `requests`, `BeautifulSoup`, `pandas`

## Usage

1. **Clone the Repository:**

    ```
    git clone https://github.com/csvaldellon/carbonara-recipe-calculator.git
    cd recipe-calculator
    ```

2. **Install Dependencies:**

    ```
    pip install -r requirements.txt
    ```

3. **Run the Script:**

    ```
    python script.py --serving_size=4
    ```

    Replace `4` with the desired serving size.

## Command-line Arguments

- `--serving_size`: Specify the serving size for the recipe (default: 4).

## Notes

- The script might require adjustments for different websites' HTML structures if used for scraping recipes from other sources.
