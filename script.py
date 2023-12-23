import argparse

from config import DEFAULT_SERVING_SIZE
from recipe_calculator import calculate_recipe


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Recipe Calculator")
    parser.add_argument(
        "--serving_size",
        type=int,
        default=DEFAULT_SERVING_SIZE,
        help="Desired serving size for the recipe (default: 4)",
    )

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
