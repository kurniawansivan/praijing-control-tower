from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.order import OrderCreate, OrderOut
from app.storage.orders import create_order, list_orders, get_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def create_order_endpoint(payload: OrderCreate) -> OrderOut:
    return create_order(payload)  # type: ignore[return-value]


@router.get("", response_model=List[OrderOut])
def list_orders_endpoint() -> List[OrderOut]:
    return list_orders()  # type: ignore[return-value]


@router.get("/{order_id}", response_model=OrderOut)
def get_order_endpoint(order_id: int) -> OrderOut:
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order  # type: ignore[return-value]
