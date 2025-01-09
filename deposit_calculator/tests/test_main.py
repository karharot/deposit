import pytest

from app.models import Deposit
from .conftest import db_session, client


@pytest.mark.asyncio
async def test_calculate_deposit_success(db_session, client):
    test_deposit_data = {
        "data": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }

    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 200
    assert response.json() == {
        "31.01.2021": 10050.00,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75,
    }
    assert db_session.query(Deposit).count() == 1
    db_deposit = db_session.query(Deposit).first()
    assert db_deposit.amount == test_deposit_data['amount']
    assert db_deposit.periods == test_deposit_data['periods']
    assert db_deposit.rate == test_deposit_data['rate']
    assert db_deposit.date == test_deposit_data['data']


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_date(db, client):
    test_deposit_data = {
        "data": "31/01/2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }

    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 400
    assert response.json() == {"error": "Invalid date format. Use DD.MM.YYYY."}
    assert db.query(Deposit).count() == 0


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_period(db, client):
    test_deposit_data = {
        "data": "31.01.2021",
        "periods": 0,
        "amount": 10000,
        "rate": 6
    }
    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 400
    assert response.json() == {"error": "Periods must be between 1 and 60"}
    assert db.query(Deposit).count() == 0


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_amount(db, client):
    test_deposit_data = {
        "data": "31.01.2021",
        "periods": 3,
        "amount": 1000,
        "rate": 6
    }
    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 400
    assert response.json() == {"error": "Amount must be between 10000 and 1000000"}
    assert db.query(Deposit).count() == 0


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_rate(db, client):
    test_deposit_data = {
        "data": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 10
    }

    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 400
    assert response.json() == {"error": "Rate must be between 1 and 8"}
    assert db.query(Deposit).count() == 0
