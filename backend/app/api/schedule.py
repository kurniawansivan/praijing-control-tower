from typing import List
from fastapi import APIRouter
from app.schemas.order import ScheduleItem
from app.storage.orders import schedule_preview

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/preview", response_model=List[ScheduleItem])
def preview_endpoint() -> List[ScheduleItem]:
    return schedule_preview()  # type: ignore[return-value]
