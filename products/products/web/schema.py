from pathlib import Path

from ariadne import make_executable_schema

from .queries import query
from .types import product_type, datetime_scalar, product_interface, supplier_type, ingredient_type
from .mutations import mutation

schema = make_executable_schema(
    (Path(__file__).parent.parent.parent / "products.graphql").read_text(), 
    [query, mutation, product_type, product_interface, supplier_type, ingredient_type, datetime_scalar]
)