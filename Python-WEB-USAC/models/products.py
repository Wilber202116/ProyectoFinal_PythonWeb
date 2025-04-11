import json
import os

PRODUCT_FILE = os.path.join("data","product.json")

def loadProducts():
    if os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, "r") as file:
            
            return json.load(file)
    return []

def saveProducts(product):
    with open(PRODUCT_FILE, "w", encoding="UTF-8") as f:
        json.dump(product, f, indent=4)

def getProductById(idProduct):
    products = loadProducts()
    return next((p for p in products if p["id"] == idProduct), None)
