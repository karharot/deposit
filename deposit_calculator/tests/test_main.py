import pytest
from .conftest import db_session


@pytest.mark.asyncio
async def test_calculate_deposit_success(db_session, client):
    test_deposit_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }

    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 200
    assert response.json() == {
        "02.03.2021": 10050,
        "01.04.2021": 10100.25,
        "01.05.2021": 10150.75
    }


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_date(db_session, client):
    test_deposit_data = {
        "date": "31/01/2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }

    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 400
    assert "time data" in response.json()['detail']['error']
    assert "does not match format '%d.%m.%Y'" in response.json()['detail'][
        'error']


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_period(db_session, client):
    test_deposit_data = {
        "date": "31.01.2021",
        "periods": 0,
        "amount": 10000,
        "rate": 6
    }
    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 422
    assert 'periods' in response.json()['detail'][0]['loc']


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_amount(db_session, client):
    test_deposit_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 1000,
        "rate": 6
    }
    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 422
    assert 'amount' in response.json()['detail'][0]['loc']
    assert 'Amount must be between 10000 and 1000000' in response.json()['detail'][0]['msg']


@pytest.mark.asyncio
async def test_calculate_deposit_invalid_rate(db_session, client):
    test_deposit_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 10
    }

    response = client.post("/calculate_deposit", json=test_deposit_data)

    assert response.status_code == 422
    assert 'rate' in response.json()['detail'][0]['loc']
    assert 'Rate must be between 1 and 8' in response.json()['detail'][0]['msg']
