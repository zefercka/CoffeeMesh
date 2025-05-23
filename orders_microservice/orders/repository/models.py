import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, ForeignKeyConstraint

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class OrderModel(Base):
    __tablename__ = 'orders'
    
    order_id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default='created', nullable=False)
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    schedule_id: Mapped[str] = mapped_column(nullable=True)
    delivery_id: Mapped[str] = mapped_column(nullable=True)
        
    items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    def dict(self):
        return {
            'id': self.order_id,
            'status': self.status,
            'created': self.created,
            'schedule_id': self.schedule_id,
            'delivery_id': self.delivery_id,
            'items': [item.dict() for item in self.items]
        }


class OrderItemModel(Base):
    __tablename__ = 'order_items'
    
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    order_id: Mapped[str] = mapped_column(
        ForeignKey('orders.order_id', ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=False
    )
    product: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    order: Mapped["OrderModel"] = relationship(back_populates="items") 
    
    def dict(self):
        return {
            'id': self.id,
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }