from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from orders.web.api.schemas import (CreateOrderSchema, GetOrderSchema,
                                GetOrdersSchema)
from orders.web.app import app

orders = []

@app.get('/orders')
def get_orders(cancelled: Optional[bool] = None, 
               limit: Optional[int] = None) -> GetOrdersSchema:
    if cancelled is None and limit is None:
        return {
            'orders': orders
        }
    
    query_set = [order for order in orders]
    
    if cancelled is not None:
        if cancelled:
            query_set = [
                order
                for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order
                for order in query_set
                if order['status'] != 'cancelled'
            ]
        
    if limit is not None and len(query_set) > limit:
        return {
            'orders': query_set[:limit]
        }
    
    return {
        'orders': query_set
    }


@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(order_details: CreateOrderSchema):
    order = order_details.model_dump()
    order['id'] = uuid4()
    order['created'] = datetime.now()
    order['status'] = 'created'
    orders.append(order)
    return order

@app.get('/orders/{order_id}')
def get_order(order_id: UUID) -> GetOrderSchema:
    for order in orders:
        if order['id'] == order_id:
            return order
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order['id'] == order_id:
            order.update(order_details.model_dump())
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order['id'] == order_id:
            orders.pop(index)
            # Используем .value чтобы вернуть пустое значение
            return Response(status_code=status.HTTP_204_NO_CONTENT.value)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'canceled'
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )


@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Order with ID {order_id} not found',
    )