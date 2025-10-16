from __future__ import annotations
from typing import Dict, Any, List
from itertools import count
from app.schemas.order import OrderCreate, Priority

# deterministic counters
_order_id_seq = count(1)
_order_item_id_seq = count(1)

# in-memory store
_ORDERS: Dict[int, Dict[str, Any]] = {}

_PRIORITY_WEIGHT = {
    Priority.urgent: 0,
    Priority.high: 1,
    Priority.normal: 2,
    Priority.low: 3,
}


def _reset_for_tests() -> None:
    """Auto-used by tests to keep isolation."""
    global _ORDERS, _order_id_seq, _order_item_id_seq
    _ORDERS = {}
    _order_id_seq = count(1)
    _order_item_id_seq = count(1)


def create_order(payload: OrderCreate) -> Dict[str, Any]:
    order_id = next(_order_id_seq)
    order = {
        "order_id": order_id,
        "source": payload.source,
        "customer_or_partner": payload.customer_or_partner,
        "priority": payload.priority,
        "status": "draft",
        "items": [],
    }
    for item in payload.items:
        order_item_id = next(_order_item_id_seq)
        order["items"].append({
            "order_item_id": order_item_id,
            "product_sku": item.product_sku,
            "quantity": int(item.quantity),
            "due_date": item.due_date,
            "status": "pending",
        })
    _ORDERS[order_id] = order
    return order


def list_orders() -> List[Dict[str, Any]]:
    return list(_ORDERS.values())


def get_order(order_id: int) -> Dict[str, Any] | None:
    return _ORDERS.get(order_id)


def schedule_preview() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for order in _ORDERS.values():
        for item in order["items"]:
            rows.append({
                "order_id": order["order_id"],
                "order_item_id": item["order_item_id"],
                "product_sku": item["product_sku"],
                "quantity": item["quantity"],
                "due_date": item["due_date"],
                "priority": order["priority"],
            })
    rows.sort(key=lambda r: (r["due_date"], _PRIORITY_WEIGHT[r["priority"]]))
    return rows
