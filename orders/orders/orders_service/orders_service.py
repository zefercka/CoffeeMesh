from orders.repository.orders_repository import OrdersRepository
from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders import Order


class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository
    
    def place_order(self, items) -> Order:
        return self.orders_repository.add(items)
    
    def get_order(self, order_id) -> Order:
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        return order


    def update_order(self, order_id, items) -> Order:
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        return self.orders_repository.update(order_id, items)
    
    def list_orders(self, **filters) -> list[Order]:
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit, **filters)
        
    def pay_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        
        order.pay()
        schedule_id = order.schedule()
        return self.orders_repository.update(
            id_=order_id, 
            payload={
                "status": "scheduled",
                "schedule_id": schedule_id,
            }
        )
    
    def cancel_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        
        order.cancel()
        return self.orders_repository.update(
            id_=order_id, status="cancelled"
        )

    def delete_order(self, order_id):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        return self.orders_repository.delete(order_id)