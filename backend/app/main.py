from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.errors import validation_error_handler
from app.api.orders import router as orders_router
from app.api.schedule import router as schedule_router

app = FastAPI(title="Praijing Control Tower")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router)
app.include_router(schedule_router)
# Validation Error Handler
app.add_exception_handler(RequestValidationError, validation_error_handler)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
