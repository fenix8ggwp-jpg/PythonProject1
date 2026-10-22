import pandas as pd
import random
from datetime import datetime, timedelta

# Генерируем данные
data = []
categories = ["Супермаркеты", "Фастфуд", "Топливо", "Развлечения", "Переводы", "Наличные", "ЖКХ"]
descriptions = ["Лента", "Макдоналдс", "Лукойл", "Кино", "Перевод другу", "Снятие в банкомате", "Оплата ЖКУ"]
statuses = ["OK", "OK", "OK", "FAILED"]
cards = ["*1234", "*5678"]

base_date = datetime(2023, 10, 1)
for i in range(50):
    date_op = base_date + timedelta(days=random.randint(0, 30))
    category = random.choice(categories)
    desc = random.choice(descriptions)

    # Расходы отрицательные, поступления положительные
    amount = round(random.uniform(100, 5000), 2)
    if category in ["Супермаркеты", "Фастфуд", "Топливо", "Развлечения", "ЖКХ", "Наличные"]:
        amount = -amount

    data.append([
        date_op, date_op, random.choice(cards), random.choice(statuses),
        amount, "RUB", amount, "RUB",
        abs(amount) * 0.01 if amount < 0 else 0, category,
        random.randint(5000, 5999), desc, 0, 0, round(amount)
    ])

# Создаем DataFrame
columns = [
    "Дата операции", "Дата платежа", "Номер карты", "Статус",
    "Сумма операции", "Валюта операции", "Сумма платежа",
    "Валюта платежа", "Кешбэк", "Категория", "MCC",
    "Описание", "Бонусы (включая кешбэк)", "Округление на «Инвесткопилку»", "Сумма операции с округлением"
]
df = pd.DataFrame(data, columns=columns)

# Сохраняем в Excel
with pd.ExcelWriter("data/operations.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, index=False)

print("Файл operations.xlsx успешно создан с 15 колонками!")