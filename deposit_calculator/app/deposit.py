from datetime import datetime, timedelta


def calculate_deposit(start_date: str, periods: int, amount: float, rate: float):
    date_format = "%d.%m.%Y"
    current_date = datetime.strptime(start_date, date_format)
    results = {}

    for _ in range(periods):
        interest = amount * (rate / 100) / 12
        amount += interest
        current_date = current_date + timedelta(days=30)
        results[current_date.strftime(date_format)] = round(amount, 2)

    return results
