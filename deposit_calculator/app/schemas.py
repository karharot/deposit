from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime


class DepositRequest(BaseModel):
    data: str
    periods: int
    amount: int
    rate: float

    @field_validator("data")
    def validate_data(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")
        return value

    @field_validator("periods")
    def validate_periods(cls, value):
        if not 1 <= value <= 60:
            raise ValueError("Periods must be between 1 and 60")
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        if not 10000 <= value <= 1000000:
            raise ValueError("Amount must be between 10000 and 1000000")
        return value

    @field_validator("rate")
    def validate_rate(cls, value):
        if not 1 <= value <= 8:
            raise ValueError("Rate must be between 1 and 8")
        return value


class DepositResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )
