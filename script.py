import sys
import argparse
from utils.ingestion import ingest_recipe
from utils.calculator import calculate_recipe
from utils.config import DEFAULT_SERVING_SIZE, VALID_UNIT_SYSTEMS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to ingest recipes and calculate servings."
    )
    parser.add_argument(
        "-ingestion", action="store_true", default=False, help="Perform ingestion."
    )
    parser.add_argument(
        "--force_ingestion",
        action="store_true",
        default=False,
        help="Force ingestion regardless if ingestion_path is already present or not.",
    )
    parser.add_argument(
        "-calculate",
        action="store_true",
        default=False,
        help="Perform recipe calculation.",
    )
    parser.add_argument(
        "--serving_size",
        type=float,
        default=DEFAULT_SERVING_SIZE,
        help=f"Desired serving size for the recipe (default: {DEFAULT_SERVING_SIZE}).",
    )
    parser.add_argument(
        "--unit_system",
        type=str,
        default=VALID_UNIT_SYSTEMS["us"],
        choices=VALID_UNIT_SYSTEMS.values(),
        help=f"Unit system to be used: {', '.join(list(VALID_UNIT_SYSTEMS.values()))}. Default is {VALID_UNIT_SYSTEMS['us']}.",
    )
    parser.add_argument(
        "--ignore_ingested_recipe",
        action="store_true",
        default=False,
        help="Ignore ingested recipe and scrapes the recipe from scratch before calculation.",
    )

    args = parser.parse_args()

    if not (args.ingestion or args.calculate):
        parser.print_help()
        sys.exit("\nPlease specify either '-ingestion' or '-calculate'.")

    if args.ingestion:
        ingest_recipe(force_ingestion=args.force_ingestion)

    if args.calculate:
        serving_size = args.serving_size
        unit_system = args.unit_system
        ignore_ingested_recipe = args.ignore_ingested_recipe
        recipe = calculate_recipe(serving_size, unit_system, ignore_ingested_recipe)
        if recipe:
            for line in recipe:
                print(line)
        else:
            print("Recipe calculation failed.")
