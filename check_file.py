import pandas as pd

# Читаем без хедера, просто чтобы увидеть сырые данные
df = pd.read_excel("operations.xlsx", header=None)
print(f"Всего строк: {len(df)}")
print(f"Всего колонок: {len(df.columns)}")
print("\nПервые 10 строк (сырые данные):")
print(df.head(10).to_string())