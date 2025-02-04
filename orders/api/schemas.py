from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint, conlist


class Size(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    
    
class Status(str, Enum):
    CREATED = "created"
    progess = "progress"
    CANCELED = "canceled"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    

class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Annotated[int, Field(ge=1, strict=True)] = 1
    
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


class GetOrdersSchema(BaseModel):
    orders: list[GetOrderSchema]