import requests
import json


class APIException(Exception):
    """Исключение, вызываемое при ошибке пользователя."""
    pass


class CurrencyConverter:
    """Класс для работы с API обмена валют."""

    API_URL = "https://api.exchangerate-api.com/v4/latest/"

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Ошибка: '{amount}' не является числом.")

        if base == quote:
            raise APIException("Ошибка: валюты должны быть разными.")

        response = requests.get(CurrencyConverter.API_URL + base.upper())

        if response.status_code != 200:
            raise APIException("Ошибка API: не удалось получить данные.")

        data = response.json()
        rates = data.get("rates", {})

        if quote.upper() not in rates:
            raise APIException(f"Ошибка: валюта '{quote}' не найдена.")

        converted_amount = rates[quote.upper()] * amount
        return f"{amount} {base.upper()} = {converted_amount:.2f} {quote.upper()}"