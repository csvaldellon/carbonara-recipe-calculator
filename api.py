from fastapi import FastAPI
from typing import List
from utils.calculator import calculate_recipe
from utils.config import DEFAULT_SERVING_SIZE

app = FastAPI()


@app.get("/calculate_recipe/")
def calculate_recipe_endpoint(serving_size: float = DEFAULT_SERVING_SIZE) -> List[str]:
    recipe = calculate_recipe(serving_size)
    if recipe:
        return recipe
    else:
        return ["Recipe calculation failed."]
