from sqlalchemy import Table, Column, Integer, String, DateTime, func
from .db import metadata

request_logs = Table(
    "request_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("operation", String, nullable=False),
    Column("input_value", String, nullable=False),
    Column("result", String, nullable=True),
    Column("status", String, nullable=False, default="pending"),
    Column("timestamp", DateTime(timezone=True), server_default=func.now(), nullable=False),
)
