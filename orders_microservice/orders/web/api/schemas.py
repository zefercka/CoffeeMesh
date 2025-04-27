from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class Size(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    
    
class Status(str, Enum):
    CREATED = "created"
    PROGRESS = "progress"
    CANCELED = "canceled"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    

class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Annotated[int, Field(ge=1, strict=True, le=100)] = 1
    
    class Config:
        extra = 'forbid'

class CreateOrderSchema(BaseModel):
    order: Annotated[list[OrderItemSchema], Field(min_items=1)]
    
    class Config:
        extra = 'forbid'
    

class GetOrderSchema(BaseModel):
    id: UUID
    created: datetime
    status: Status
    order: list[OrderItemSchema]


class GetOrdersSchema(BaseModel):
    orders: list[GetOrderSchema]