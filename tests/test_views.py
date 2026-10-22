from datetime import datetime
from src.views import get_greeting, get_cards_info, get_top_transactions


def test_get_greeting():
    assert get_greeting(datetime(2023, 1, 1, 8, 0)) == "Доброе утро"
    assert get_greeting(datetime(2023, 1, 1, 14, 0)) == "Добрый день"
    assert get_greeting(datetime(2023, 1, 1, 20, 0)) == "Добрый вечер"
    assert get_greeting(datetime(2023, 1, 1, 2, 0)) == "Доброй ночи"


def test_get_cards_info(sample_df):
    cards = get_cards_info(sample_df)
    # Игнорируем FAILED статус
    assert len(cards) == 2
    # Проверяем карту *1234 (траты: 1000 + 500 = 1500, кешбэк 15)
    card_1234 = next(c for c in cards if c["last_digits"] == "1234")
    assert card_1234["total_spent"] == 1500.0
    assert card_1234["cashback"] == 15.0


def test_get_top_transactions(sample_df):
    top = get_top_transactions(sample_df)
    assert len(top) == 4 # в датафрейме всего 4 транзакции
    # Самая большая трата -2000 (Переводы)
    assert top[0]["amount"] == -300.0
    assert top[0]["category"] == "Супермаркеты"