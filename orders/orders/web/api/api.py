from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from orders.web.api.schemas import (CreateOrderSchema, GetOrderSchema,
                                GetOrdersSchema)
from orders.web.app import app

from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders_service import OrdersService
from orders.repository.orders_repository import OrdersRepository
from orders.repository.unit_of_work import UnitOfWork



orders = []

@app.get('/orders')
def get_orders(cancelled: Optional[bool] = None, 
               limit: Optional[int] = None) -> GetOrdersSchema:
    with UnitOfWork() as uow:
        repo = OrdersRepository(uow.session)
        orders_service = OrdersService(repo)
        
        results = orders_service.list_orders(
            limit=limit, cancelled=cancelled
        )
        
    return {
        'orders': [result.dict() for result in results]
    }


@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(order_details: CreateOrderSchema) -> GetOrderSchema:
    with UnitOfWork() as uow:
        repo = OrdersRepository(uow.session)
        orders_service = OrdersService(repo)
        
        order = order_details.model_dump()['order']
        
        print(order.items[0]["size"])
        
        order = orders_service.place_order(order)
        uow.commit()
    
    return order.dict()
        

@app.get('/orders/{order_id}')
def get_order(order_id: UUID) -> GetOrderSchema:
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            order = orders_service.get_order(order_id)
        return order.dict()
    
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order with ID {order_id} not found',
        )


@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            items = order_details.model_dump()["order"]
            
            print(type(items))
            
            order = orders_service.update_order(
                order_id=order_id, items=items
            )
            
            uow.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with ID {order_id} not found",
        )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            orders_service.delete_order(order_id=order_id)
            uow.commit()
        return
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with ID {order_id} not found",
        )


@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            orders_service.cancel_order(order_id=order_id)
            uow.commit()
        return
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with ID {order_id} not found",
        )


@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            order = orders_service.pay_order(order_id=order_id)
            uow.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order with ID {order_id} not found',
        )