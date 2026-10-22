import json
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    try:
        # Читаем файл (теперь pandas сам отлично видит все 15 колонок)
        df = pd.read_excel(file_path)

        # Преобразуем колонку с датой в формат datetime
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

        logger.info(f"Успешно загружено {len(df)} транзакций из {file_path}")
        return df
    except Exception as e:
        logger.error(f"Ошибка чтения файла {file_path}: {e}")
        raise


def load_user_settings(file_path: str) -> dict[str, Any]:
    """Загружает настройки пользователя (валюты, акции)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)