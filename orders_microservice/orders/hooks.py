import json
import dredd_hooks
import requests

response_stash = {}


@dredd_hooks.after("/orders > Creates a new order > 201 > application/json")
def save_created_order(transaction):
    response_payload = transaction["real"]["body"]
    order_id = json.loads(response_payload)["id"]
    
    response_stash["created_order_id"] = order_id


@dredd_hooks.before(
    "/orders/{order_id} > Returns the details of a specific order > 200 > application/json"
)
def before_get_order(transaction):
    transaction["fullPath"] = (
        f"/orders/{response_stash['created_order_id']}"
    )
    transaction["request"]["uri"] = (
        f"/orders/{response_stash['created_order_id']}"
    )


@dredd_hooks.before(
    "/orders/{order_id} > Replaces an existing order > 200 > application/json"
)
def before_put_order(transaction):
    transaction["fullPath"] = (
        f"/orders/{response_stash['created_order_id']}"
    )
    transaction["request"]["uri"] = (
        f"/orders/{response_stash['created_order_id']}"
    )


@dredd_hooks.before(
    "/orders/{order_id} > Deletes an existing order > 204"
)
def before_delete_order(transaction):
    transaction["fullPath"] = (
        f"/orders/{response_stash['created_order_id']}"
    )
    transaction["request"]["uri"] = (
        f"/orders/{response_stash['created_order_id']}"
    )


@dredd_hooks.before(
    "/orders/{order_id}/pay > Processes payment for an order > 200 > application/json"
)
def before_pay_order(transaction):
    response = requests.post(
        url="http://127.0.0.1:8000/orders",
        json={
            "order": [
                {
                    "product": "string",
                    "size": "small",
                    "quantity": 1,
                }
            ]
        }
    )

    id_ = response.json()["id"]
    transaction["fullPath"] = (
        f"/orders/{id_}/pay"
    )
    transaction["request"]["uri"] = (
        f"/orders/{id_}/pay"
    )
    

@dredd_hooks.before(
    "/orders/{order_id}/cancel > Cancels an order > 200 > application/json"
)
def before_cancel_order(transaction):
    response = requests.post(
        url="http://127.0.0.1:8000/orders",
        json={
            "order": [
                {
                    "product": "string",
                    "size": "small",
                    "quantity": 1,
                }
            ]
        }
    )

    id_ = response.json()["id"]
    transaction["fullPath"] = (
        f"/orders/{id_}/cancel"
    )
    transaction["request"]["uri"] = (
        f"/orders/{id_}/cancel"
    )
    

@dredd_hooks.before(
    '/orders > Creates a new order > 422 > application/json'
)
def fail_create_order(transaction):
    transaction["request"]["body"] = json.dumps(
        {
            "order": [
                {
                    "product": "string",
                    "size": "no size"
                }
            ]
        }
    )
    

@dredd_hooks.before(
    "/orders > Get all orders > 422 > application/json"
)
def fail_get_orders(transaction):
    transaction["request"]["uri"] = (
        f"/orders?limit=dfgdf"
    )
    transaction["fullPath"] = (
        f"/orders?limit=dfgdf"
    )


@dredd_hooks.before( 
    "/orders/{order_id} > Returns the details of a specific order > 422 > application/json"
)
@dredd_hooks.before( 
    "/orders/{order_id}/cancel > Cancels an order > 422 > application/json"
)
@dredd_hooks.before( 
    "/orders/{order_id}/pay > Processes payment for an order > 422 > application/json"
)
@dredd_hooks.before( 
    "/orders/{order_id} > Replaces an existing order > 422 > application/json"
)
@dredd_hooks.before( 
    "/orders/{order_id} > Deletes an existing order > 422 > application/json"
)
def fail_target_specific_order(transaction): 
    transaction["fullPath"] = transaction["fullPath"].replace( 
        "d44ba540-7919-408b-8505-6166702430da", "8" 
    )
    
    transaction["request"]["uri"] = transaction["request"]["uri"].replace( 
        "d44ba540-7919-408b-8505-6166702430da", "8" 
    ) 
