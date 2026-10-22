import json
import logging
from datetime import datetime
from typing import Any

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 6 <= hour <= 11:
        return "Доброе утро"
    elif 12 <= hour <= 17:
        return "Добрый день"
    elif 18 <= hour <= 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Считает траты и кешбэк по каждой карте."""
    # Берем только валидные операции
    valid_ops = df[df["Статус"] == "OK"].copy()

    # Группируем по последним 4 цифрам карты
    cards = []
    grouped = valid_ops.groupby("Номер карты")

    for card, group in grouped:
        # Траты — это отрицательные суммы, берем их по модулю
        total_spent = abs(group[group["Сумма платежа"] < 0]["Сумма платежа"].sum())
        cashback = round(total_spent / 100, 2)

        # Убираем звездочку из номера карты, если она есть
        last_digits = str(card).replace("*", "")

        cards.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": cashback
        })
    return cards


def get_top_transactions(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Возвращает топ-5 транзакций по сумме платежа."""
    top5 = df.nlargest(5, "Сумма платежа")
    result = []
    for _, row in top5.iterrows():
        # Форматируем дату из строки в нужный формат (если она строка)
        dt = pd.to_datetime(row["Дата операции"], dayfirst=True)
        result.append({
            "date": dt.strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"]
        })
    return result


def get_currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """Получает курсы валют (заглушка для API)."""
    # В реальном проекте тут requests.get("...")
    # Для тестов возвращаем фиксированные данные
    rates = {"USD": 90.5, "EUR": 98.2}
    result = []
    for cur in currencies:
        result.append({"currency": cur, "rate": rates.get(cur, 1.0)})
    return result


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Получает цены на акции (заглушка для API)."""
    prices = {"AAPL": 175.5, "AMZN": 180.2, "GOOGL": 150.3, "MSFT": 400.1, "TSLA": 200.0}
    result = []
    for stock in stocks:
        result.append({"stock": stock, "price": prices.get(stock, 100.0)})
    return result


def main_page(date_str: str, df: pd.DataFrame, settings: dict) -> str:
    """Генерирует JSON для главной страницы."""
    # Парсим входную дату
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Фильтруем данные с начала месяца по эту дату
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0)

    filtered_df = df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= dt)]

    response = {
        "greeting": get_greeting(dt),
        "cards": get_cards_info(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"])
    }

    return json.dumps(response, ensure_ascii=False, indent=2)