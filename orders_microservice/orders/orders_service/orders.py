from ..repository.models import OrderModel
from datetime import datetime
from typing import Iterable
import requests

from .exceptions import (
    APIIntegrationError, InvalidActionError, ExternalServiceUnavailableError
)

from requests.exceptions import ConnectionError


class OrderItem:
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size
        
    def dict(self):
        return {
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }


class Order:
    def __init__(self, id, created: datetime, items: Iterable, status: str,
                 schedule_id=None, delivery_id=None,
                 order_: OrderModel=None):
        self._order = order_
        self._id = id
        self._created = created
        self.items = [OrderItem(**item) for item in items]
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id
    
    @property
    def id(self):
        return self._id or self._order.order_id
    
    @property
    def created(self):
        return self._created or self._order.created
    
    @property
    def status(self):
        return self._status or self._order.status
    
    def cancel(self):
        if self.status == 'progress':
            kitchen_base__url = "http://127.0.0.1:3001/kitchen"

            try:
                response = requests.post(
                    f'{kitchen_base__url}/schedules/{self.schedule_id}/cancel',
                    json={
                        "order": [item.dict() for item in self.items],
                    }
                )
            except ConnectionError as error:
                raise ExternalServiceUnavailableError
            
            if response.status_code == 200:
                return
            
            raise APIIntegrationError(
                f"Couldn't cancel order with id {self.id}"
            )
        
        if self.status == 'delivery':
            raise InvalidActionError(
                f"Can't cancel order with id {self.id} because it's already in delivery status"
            )

    def pay(self):
        try:
            response = requests.post(
                'http://127.0.0.1:3000/payments',
                json={
                    "order_id": self.id
                }
            )
        except ConnectionError as error:
            raise ExternalServiceUnavailableError

        if response.status_code == 201:
            return
        
        raise APIIntegrationError(
            f"Couldn't process payment for order with id {self.id}"
        )
    
    def schedule(self):
        try:
            response = requests.post(
                'http://127.0.0.1:5000/kitchen/schedules',
                json={
                    "order": [item.dict() for item in self.items],
                }
            )
        except ConnectionError as error:
            print(error)
            raise ExternalServiceUnavailableError
        
        if response.status_code == 201:
            return
        
        raise APIIntegrationError(
            f"Couldn't schedule order with id {self.id}"    
        )
    
    def dict(self):
        return {
            'id': self.id,
            'order': [item.dict() for item in self.items],
            'status': self.status,
            'created': self.created,
        }