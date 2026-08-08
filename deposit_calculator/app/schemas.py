from pydantic import BaseModel, field_validator, ConfigDict


class DepositRequest(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("date")
    def validate_date(cls, value: str):
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
