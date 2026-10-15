# Task 2: Load Data from JSON

import json
import pandas as pd

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 65000
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 30000
    },
    {
        "id": 3,
        "name": "Tablet",
        "price": 25000
    }
]

with open("products.json", "w") as file:
    json.dump(products, file, indent=4)

df = pd.read_json("products.json")

print(df)