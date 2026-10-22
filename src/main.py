import json
from src.utils import load_transactions, load_user_settings
from src.views import main_page
from src.services import simple_search, phone_search
from src.reports import spending_by_category


def main():
    # Загрузка данных
    df = load_transactions("data/operations.xlsx")
    settings = load_user_settings("user_settings.json")

    # 1. Главная страница (на 10 октября 2023)
    print("=== ГЛАВНАЯ СТРАНИЦА ===")
    view_json = main_page("2023-10-10 14:30:00", df, settings)
    print(view_json)

    # 2. Поиск
    print("\n=== ПОИСК ПО ТЕЛЕФОНУ ===")
    phones = phone_search(df)
    print(phones)

    # 3. Отчет (сохранится в файл report_spending_by_category_...json)
    print("\n=== ОТЧЕТ ===")
    report = spending_by_category(df, "Супермаркеты", "2023-10-10")
    print(f"Найдено {len(report)} транзакций. Отчет сохранен в файл.")


if __name__ == "__main__":
    main()