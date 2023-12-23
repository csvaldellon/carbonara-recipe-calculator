from fastapi import FastAPI
from typing import Optional
from utils.ingestion import ingest_recipe
from utils.calculator import calculate_recipe
from utils.config import DEFAULT_SERVING_SIZE, VALID_UNIT_SYSTEMS

app = FastAPI()


@app.get("/ingest_recipe")
def ingest_recipe_endpoint(force_ingestion: Optional[bool] = False):
    ingest_recipe(force_ingestion=force_ingestion)
    return {"message": "Recipe ingested successfully"}


@app.get("/calculate_recipe")
def calculate_recipe_endpoint(
    serving_size: Optional[float] = DEFAULT_SERVING_SIZE,
    unit_system: Optional[str] = VALID_UNIT_SYSTEMS["us"],
    ignore_ingested_recipe: Optional[bool] = False,
):
    recipe = calculate_recipe(serving_size, unit_system, ignore_ingested_recipe)
    if recipe:
        return {"recipe": recipe}
    else:
        return {"message": "Recipe calculation failed"}
