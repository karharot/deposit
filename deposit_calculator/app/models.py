from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, Float
from app.base_model import Base


class Deposit(Base):

    date: Mapped[str] = mapped_column(String)
    periods: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)
    rate: Mapped[float] = mapped_column(Float)
