from ..repository.orders_repository import OrdersRepository
from .exceptions import OrderNotFoundError
from .orders import Order
from ..web.api.schemas import Status


class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository
    
    def place_order(self, items, user_id) -> Order:
        return self.orders_repository.add(items, user_id)
    
    def get_order(self, order_id, **filters) -> Order:
        order = self.orders_repository.get(order_id, **filters)
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        return order

    def update_order(self, order_id, user_id, **payload) -> Order:
        order = self.orders_repository.get(
            id_=order_id,
            user_id=user_id,
        )
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        return self.orders_repository.update(order_id, **payload)
    
    def list_orders(self, **filters) -> list[Order]:
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit, **filters)
        
    def pay_order(self, order_id, user_id) -> Order:
        order = self.orders_repository.get(
            id_=order_id,
            user_id=user_id
        )
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        
        # order.pay()
        schedule_id = order.schedule()
        return self.orders_repository.update(
            id_=order_id, 
            payload={
                "status": Status.PROGRESS.value,
                "schedule_id": schedule_id,
            }
        )
    
    def cancel_order(self, order_id, user_id) -> Order:
        order = self.orders_repository.get(
            id_=order_id,
            user_id=user_id,
        )
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        
        order.cancel()
        return self.orders_repository.update(
            id_=order_id,
            status=Status.CANCELED.value,
        )

    def delete_order(self, order_id, user_id) -> None:
        order = self.orders_repository.get(
            id_=order_id,
            user_id=user_id,
        )
        if order is None:
            raise OrderNotFoundError(
                f"Order with id {order_id} not found"
            )
        return self.orders_repository.delete(order_id)