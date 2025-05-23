from pathlib import Path

from hypothesis import strategies as st
import jsonschema
import yaml
from fastapi.testclient import TestClient
from hypothesis import given, Verbosity, settings
from jsonschema import ValidationError, RefResolver

from .web.app import app

orders_api_spec = yaml.full_load(
    (Path(__file__).parent.parent / "oas.yaml").read_text()
)
create_order_schema = (
    orders_api_spec["components"]["schemas"]["CreateOrderSchema"]
)


def is_valid_payload(payload, schema):
    try:
        jsonschema.validate(
            payload, schema=schema, resolver=RefResolver('', orders_api_spec)
        )
    except ValidationError:
        return False
    else:
        return True


test_client = TestClient(app=app)

values_strategy = (
    st.none() |
    st.booleans() |
    st.text() |
    st.integers()
)

order_item_strategy = st.fixed_dictionaries(
    {
        "product": values_strategy,
        "size": st.one_of(st.sampled_from(("small", "medium", "big"))) | values_strategy,
        "quantity": values_strategy,
    }
)

strategy = st.fixed_dictionaries(
    {
        "order": st.lists(order_item_strategy)
    }
)

@given(strategy)
def test(payload):
    response = test_client.post("/orders", json=payload)
    
    if is_valid_payload(payload, create_order_schema):
        print(response.status_code)
        assert response.status_code == 201
    else:
        print(response.status_code)
        assert response.status_code == 422