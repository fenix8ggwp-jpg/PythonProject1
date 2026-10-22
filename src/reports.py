import functools
import json
from datetime import datetime, timedelta
from typing import Callable, Optional

import pandas as pd


def save_to_file(file_name: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата отчета в файл."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Определяем имя файла
            fname = file_name or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Если результат — DataFrame, переводим в JSON-строку
            if isinstance(result, pd.DataFrame):
                data_to_save = result.to_json(orient="records", force_ascii=False, indent=2)
            elif isinstance(result, (dict, list)):
                data_to_save = json.dumps(result, ensure_ascii=False, indent=2)
            else:
                data_to_save = str(result)

            with open(fname, "w", encoding="utf-8") as f:
                f.write(data_to_save)

            return result

        return wrapper

    return decorator


@save_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние 3 месяца."""
    if date:
        end_date = pd.to_datetime(date, dayfirst=True)
    else:
        end_date = pd.to_datetime(datetime.now())

    start_date = end_date - timedelta(days=90)

    # Убедимся, что колонка с датой — datetime
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])

    # Фильтруем по датам и категории
    mask = (transactions["Дата операции"] >= start_date) & \
           (transactions["Дата операции"] <= end_date) & \
           (transactions["Категория"] == category)

    # Берем только траты (отрицательные суммы)
    result = transactions[mask & (transactions["Сумма платежа"] < 0)]

    return result