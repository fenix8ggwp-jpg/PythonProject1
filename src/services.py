import json
import re
from typing import Any

import pandas as pd


def simple_search(df: pd.DataFrame, query: str) -> str:
    """Ищет транзакции по подстроке в описании или категории."""
    mask = df["Описание"].str.contains(query, case=False, na=False) | \
           df["Категория"].str.contains(query, case=False, na=False)

    result_df = df[mask]
    records = result_df.to_dict(orient="records")
    return json.dumps(records, ensure_ascii=False, indent=2)


def phone_search(df: pd.DataFrame) -> str:
    """Ищет транзакции, содержащие мобильные номера в описании."""
    # Ищем просто наличие цифр в формате +7... или 8...
    # Используем регулярное выражение без сложных групп захвата
    pattern = r"[+8]\d[\s\-\(\)0-9]{9,15}"

    # Применяем поиск к каждой строке
    mask = df["Описание"].astype(str).apply(lambda x: bool(re.search(pattern, x)))

    result_df = df[mask]
    records = result_df.to_dict(orient="records")
    return json.dumps(records, ensure_ascii=False, indent=2)