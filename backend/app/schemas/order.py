from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt
from pydantic.types import StringConstraints

# Reusable constrained string: non-empty, trims whitespace
NonEmptyStr = Annotated[str, StringConstraints(
    strip_whitespace=True, min_length=1)]


class Priority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class OrderItemCreate(BaseModel):
    product_sku: NonEmptyStr = Field(...)
    quantity: PositiveInt = Field(...)
    due_date: date = Field(...)


class OrderCreate(BaseModel):
    source: NonEmptyStr = Field(...)
    customer_or_partner: NonEmptyStr = Field(...)
    priority: Priority = Priority.normal
    items: list[OrderItemCreate] = Field(...)


class OrderItemOut(BaseModel):
    order_item_id: int
    product_sku: str
    quantity: int
    due_date: date
    status: str


class OrderOut(BaseModel):
    order_id: int
    source: str
    customer_or_partner: str
    priority: Priority
    status: str
    items: list[OrderItemOut]


class ScheduleItem(BaseModel):
    order_id: int
    order_item_id: int
    product_sku: str
    quantity: int
    due_date: date
    priority: Priority
