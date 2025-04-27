from typing import Optional
from uuid import UUID

import json

from fastapi import HTTPException, Request, status

from .schemas import (
    CreateOrderSchema, GetOrderSchema, GetOrdersSchema
)
from ..app import app

from ...orders_service.exceptions import (
    OrderNotFoundError, BadRequestError
)
from ...orders_service.orders_service import OrdersService
from ...repository.orders_repository import OrdersRepository
from ...repository.unit_of_work import UnitOfWork


@app.get('/orders')
def get_orders(
        request: Request,
        cancelled: Optional[bool] = None,
        limit: Optional[int] = None,
) -> GetOrdersSchema:
    if limit is not None and limit <= 0:
        raise BadRequestError(
            "Limit must be positive"
        )

    with UnitOfWork() as uow:
        repo = OrdersRepository(uow.session)
        orders_service = OrdersService(repo)
        
        results = orders_service.list_orders(
            limit=limit,
            cancelled=cancelled,
            user_id=request.state.user_id
        )

    return GetOrdersSchema.model_validate(
        {
            'orders': [result.dict() for result in results]
        }
    )


@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(
        request: Request,
        order_details: CreateOrderSchema
) -> GetOrderSchema:
    with UnitOfWork() as uow:
        repo = OrdersRepository(uow.session)
        orders_service = OrdersService(repo)

        order = orders_service.place_order(
            order_details.order, request.state.user_id
        )
        uow.commit()

        return GetOrderSchema.model_validate(order.dict())
        

@app.get('/orders/{order_id}')
def get_order(
        request: Request,
        order_id: UUID
) -> GetOrderSchema:
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            print(order_id)
            
            order = orders_service.get_order(
                order_id=order_id,
                user_id=request.state.user_id,
            )
        return order.dict()
    
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )


@app.put('/orders/{order_id}')
def update_order(
        request: Request,
        order_id: UUID,
        order_details: CreateOrderSchema,
) -> GetOrderSchema:
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)

            print(
                order_id,
                order_details
            )

            order = orders_service.update_order(
                order_id=order_id,
                items=order_details.order,
                user_id=request.state.user_id
            )
            
            uow.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
        request: Request,
        order_id: UUID,
) -> None:
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            orders_service.delete_order(
                order_id=order_id,
                user_id=request.state.user_id,
            )
            uow.commit()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with ID {order_id} not found",
        )


@app.post('/orders/{order_id}/cancel')
def cancel_order(
        request: Request,
        order_id: UUID,
) -> GetOrderSchema:
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            order = orders_service.cancel_order(
                order_id=order_id,
                user_id=request.state.user_id,
            )
            uow.commit()
            
            return GetOrderSchema.model_validate(order.dict())
            
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with ID {order_id} not found",
        )


@app.post('/orders/{order_id}/pay')
def pay_order(
        request: Request,
        order_id: UUID,
) -> GetOrderSchema:
    try:
        with UnitOfWork() as uow:
            repo = OrdersRepository(uow.session)
            orders_service = OrdersService(repo)
            
            order = orders_service.pay_order(
                order_id=order_id,
                user_id=request.state.user_id
            )
            uow.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found",
        )