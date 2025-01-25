from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from orders.api.schemas import (CreateOrderSchema, GetOrderSchema,
                                GetOrdersSchema)
from orders.app import app

ORDERS = []

@app.get('/orders')
def get_orders() -> GetOrdersSchema:
    return ORDERS


@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(order_details: CreateOrderSchema):
    order = order_details.model_dump()
    order['id'] = UUID.uuid4()
    order['created'] = datetime.now()
    order['status'] = 'created'
    ORDERS.append(order)
    return order

@app.get('/orders/{order_id}')
def get_order(order_id: UUID) -> GetOrderSchema:
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.model_dump())
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            # Используем .value чтобы вернуть пустое значение
            return Response(status_code=status.HTTP_204_NO_CONTENT.value)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'canceled'
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )