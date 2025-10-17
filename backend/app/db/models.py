from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.schemas.order import Priority

# Order Model (Orders table)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    customer_or_partner = Column(String)
    priority = Column(Enum(Priority), default=Priority.normal)
    status = Column(String, default="draft")

    items = relationship("OrderItem", back_populates="order")


# OrderItem Model (Order Items table)
class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    product_sku = Column(String, index=True)
    quantity = Column(Integer)
    due_date = Column(Date)
    status = Column(String, default="pending")

    order_id = Column(Integer, ForeignKey("orders.order_id"))

    order = relationship("Order", back_populates="items")


# WorkOrder Model (Work Orders table)
class WorkOrder(Base):
    __tablename__ = "work_orders"

    work_order_id = Column(Integer, primary_key=True, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.order_item_id"))
    artisan_id = Column(Integer)
    status = Column(String, default="assigned")
    started_at = Column(Date, nullable=True)
    finished_at = Column(Date, nullable=True)

    order_item = relationship("OrderItem")
