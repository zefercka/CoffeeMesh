from copy import deepcopy

from ariadne import QueryType

from itertools import islice

from .data import ingredients, products

query = QueryType()


def get_page(items, items_per_page, page):
    page = page - 1
    start = items_per_page * page
    stop = start + items_per_page
    print(islice(items, start, stop))
    return list(islice(items, start, stop))


@query.field("allIngredients")
def resolve_all_ingredients(*_):
    return ingredients


@query.field("allProducts")
def resolve_all_products(*_):
    return products


@query.field("products")
def resolve_products(*_, input=None):
    if input is None:
        return products

    filtered = [
        product for product in products
        if product["available"] is input["available"]
    ]

    if input.get("minPrice") is not None:
        filtered = [
            product for product in filtered
            if product["price"] >= input["minPrice"]
        ]

    if input.get("maxPrice") is not None:
        filtered = [
            product for product in filtered
            if product["price"] <= input["maxPrice"]
        ]

    filtered.sort(
        key=lambda product: product.get(input["sortBy"], 0),
        reverse=input["sort"] == "DESCENDING"
    )

    return get_page(filtered, input["resultsPerPage"], input["page"])


@query.field("product")
def resolve_product(*_, id: str):
    for product in products:
        if product["id"] == id:
            return product


@query.field("ingredient")
def resolve_ingredient(*_, id: str):
    for ingredient in ingredients:
        if ingredient["id"] == id:
            return ingredient