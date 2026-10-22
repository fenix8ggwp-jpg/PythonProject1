from datetime import datetime
from src.reports import spending_by_category


def test_spending_by_category(sample_df):
    # Ищем траты на Супермаркеты на дату 2023-10-10
    # За последние 90 дней попадут транзакции за 01, 02 и 05 октября
    result = spending_by_category(sample_df, "Супермаркеты", "2023-10-10")
    assert len(result) == 3
    assert result["Сумма платежа"].sum() == -1800.0 # -1000 -500 -300