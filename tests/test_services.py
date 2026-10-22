import json
from src.services import simple_search, phone_search


def test_simple_search(sample_df):
    res = simple_search(sample_df, "супер")
    data = json.loads(res)
    assert len(data) == 3 # 3 транзакции с категорией Супермаркеты


def test_phone_search(sample_df):
    res = phone_search(sample_df)
    data = json.loads(res)
    assert len(data) == 1
    assert "МТС" in data[0]["Описание"]