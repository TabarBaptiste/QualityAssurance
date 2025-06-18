from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import random

app = FastAPI()

@app.get("")
def read_root():
    return {"Status": "OK"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def get_random_french_football_club():
    clubs = [
        "PSG",
        "Lyon",
        "Marseille",
        "Nice",
        "Montpellier",
        "Strasbourg",
        "Nantes",
        "Toulouse",
        "Rennes",
        "Bordeaux"
    ]

    return random.choice(clubs)

def test_get_random_french_football_club():
    # assert get_random_french_football_club() == "Bordeaux"


    assert get_random_french_football_club() in [
        "PSG",
        "Lyon",
        "Marseille",
        "Nice",
        "Montpellier",
        "Strasbourg",
        "Nantes",
        "Toulouse",
        "Rennes",
        "Bordeaux"
    ]
