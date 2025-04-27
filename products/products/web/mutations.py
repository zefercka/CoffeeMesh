import uuid
from datetime import datetime

from ariadne import MutationType

from .data import products, suppliers, ingredients

mutation = MutationType()

@mutation.field("addProduct")
def resolve_add_product(*_, name, type: str, input: dict):
    product = {
        "id": uuid.uuid4(),
        "name": name,
        "available": input.get("available", False),
        "ingredients": input.get("ingredients", False),
        "lastUpdated": datetime.now(),
    }

    if type == "cake":
        product.update({
            "hasFilling": input["hasFilling"],
            "hasNutsToppingOption": input["hasNutsToppingOption"],
        })
    elif type == "beverage":
        product.update({
            "hasCreamOnTopOption": input["hasCreamOnTopOption"],
            "hasServeOnIceOption": input["hasServeOnIceOption"],
        })

    products.append(product)

    return product


@mutation.field("addSupplier")
def resolve_add_supplier(*_, name: str, input: dict):
    input.update({
        "id": uuid.uuid4(),
        "name": name,
    })

    suppliers.append(input)

    return input


@mutation.field("addIngredient")
def resolve_add_ingredient(*_, name: str, input: dict):
    # Нужна проверка на существование поставщика

    input.update({
        "id": uuid.uuid4(),
        "name": name,
        "lastUpdated": datetime.now(),
    })

    ingredients.append(input)

    return input

