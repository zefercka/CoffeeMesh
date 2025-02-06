from orders.orders_service.orders import Order
from orders.repository.models import OrderModel, OrderItemModel

from sqlalchemy.orm import Session 


class OrdersRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, items) -> Order:
        record = OrderModel(
            items=[OrderItemModel(**item) for item in items]
        )
        
        self.session.add(record)
        return Order(**record.dict(), order_=record)
    
    def _get(self, id_) -> OrderModel | None:
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.order_id == str(id_))
            .first()  
        )
    
    def get(self, id_) -> Order | None:
        order = self._get(id_)
        if order is not None:
            return Order(**order.dict())
    
    def list(self, limit: int | None = None, **filters) -> list[Order]:
        query = self.session.query(OrderModel)
        
        if 'cancelled' in filters:
            cancelled = filters.pop('cancelled')
            
            if cancelled:
                query = query.filter(OrderModel.status == 'cancelled')
            else:
                query = query.filter(OrderModel.status != 'cancelled')
            
        records = query.filter_by(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]
        
    def update(self, id_, payload: dict) -> Order:
        record = self._get(id_)
        
        if 'items' in payload:
            for item in record.items:
                self.session.delete(item)
            record.items = [
                OrderItemModel(**item) for item in payload.pop('items')
            ]
            
        for key, value in payload.values():
            setattr(record, key, value)
        
        return Order(**record.dict())
            
    def delete(self, id_) -> None:
        self.session.delete(self._get(id_))
