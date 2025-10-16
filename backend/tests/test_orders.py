from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_order_and_list() -> None:
    payload = {
        "source": "online",
        "customer_or_partner": "Partner A",
        "priority": "normal",
        "items": [
            {
                "product_sku": "SKU-001",
                "quantity": 3,
                "due_date": (date.today() + timedelta(days=3)).isoformat(),
            }
        ],
    }
    r = client.post("/orders", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["order_id"] >= 1
    assert data["items"][0]["order_item_id"] >= 1
    assert data["items"][0]["product_sku"] == "SKU-001"

    r2 = client.get("/orders")
    assert r2.status_code == 200
    assert len(r2.json()) == 1


def test_schedule_preview_sorting_by_due_date_then_priority() -> None:
    today = date.today()
    # order A: due in 2 days, priority normal
    client.post("/orders", json={
        "source": "online",
        "customer_or_partner": "A",
        "priority": "normal",
        "items": [{"product_sku": "A1", "quantity": 1, "due_date": (today + timedelta(days=2)).isoformat()}],
    })
    # order B: due in 2 days, priority urgent (should come before normal)
    client.post("/orders", json={
        "source": "online",
        "customer_or_partner": "B",
        "priority": "urgent",
        "items": [{"product_sku": "B1", "quantity": 1, "due_date": (today + timedelta(days=2)).isoformat()}],
    })
    # order C: due in 1 day (should come first overall)
    client.post("/orders", json={
        "source": "online",
        "customer_or_partner": "C",
        "priority": "low",
        "items": [{"product_sku": "C1", "quantity": 1, "due_date": (today + timedelta(days=1)).isoformat()}],
    })

    r = client.get("/schedule/preview")
    assert r.status_code == 200
    items = r.json()
    # expected order: C (1 day), then B (2 days urgent), then A (2 days normal)
    assert [i["product_sku"] for i in items] == ["C1", "B1", "A1"]
