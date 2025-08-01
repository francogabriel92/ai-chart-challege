from sqlmodel import SQLModel, Field, Index, text
from typing import Optional
from datetime import datetime


class Sale(SQLModel, table=True):
    __tablename__ = "sales"

    id: Optional[int] = Field(default=None, primary_key=True)

    date: datetime = Field(index=True)
    week_day: str = Field(index=True)

    ticket_number: str
    waiter: str

    product_name: str = Field(index=True)
    quantity: float
    unitary_price: float
    total: float
