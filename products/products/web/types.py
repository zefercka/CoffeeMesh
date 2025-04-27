import copy
from datetime import datetime

from ariadne import UnionType, ScalarType, InterfaceType, ObjectType

from .data import ingredients, suppliers

product_type = UnionType("Product")

supplier_type = ObjectType("Supplier")
ingredient_type = ObjectType("Ingredient")

product_interface = InterfaceType("ProductInterface")

datetime_scalar = ScalarType("Datetime")

@product_type.type_resolver
def resolve_product_type(obj, *_):
    if "hasFilling" in obj:
        return "Cake"
    return "Beverage"


@datetime_scalar.serializer
def serialize_datetime_scalar(date):
    return date.isoformat()


@datetime_scalar.value_parser
def parse_datetime_scalar(date: str):
    return datetime.fromisoformat(date)


@product_interface.field("ingredients")
def resolve_product_ingredients(product: dict, _):
    recipe = [
        copy.copy(ingredient)
        for ingredient in product.get("ingredients", [])
    ]

    for ingredient_recipe in recipe:
        for ingredient in ingredients:
            if ingredient["id"] == ingredient_recipe["ingredient"]:
                ingredient_recipe["ingredient"] = ingredient

    return recipe


@ingredient_type.field("supplier")
def resolve_ingredient_supplier(ingredient: dict, _):
    if ingredient.get("supplier") is not None:
        for supplier in suppliers:
            if supplier["id"] == ingredient["supplier"]:
                print(supplier)
                return supplier


@supplier_type.field("ingredients")
def resolve_supplier_ingredients(supplier: dict, _):
    supplier_ingredients = [
        ingredient
        for ingredient in ingredients
        if ingredient["supplier"] == supplier["id"]
    ]

    return supplier_ingredients