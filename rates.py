import csv
import os
import sys
from datetime import datetime, timedelta

import requests

URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
CURRENCIES = ["USD", "EUR", "PLN"]
FILE = "rates.csv"


def get_rates(currencies, date=None):
    params = {"json": ""}
    if date:
        params["date"] = date  # формат ГГГГММДД
    r = requests.get(URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {item["cc"]: item for item in data if item["cc"] in currencies}


def load_existing():
    """Возвращает набор уже записанных пар (дата, валюта)."""
    if not os.path.exists(FILE):
        return set()
    with open(FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)  # пропускаем заголовок
        return {(row[0], row[1]) for row in reader if len(row) >= 2}


def save_rows(rows):
    new_file = not os.path.exists(FILE)
    with open(FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if new_file:
               writer.writerow(["Date", "Currency", "Rate", "Change"])
        writer.writerows(rows)


def main():
    try:
        today = get_rates(CURRENCIES)
        date_str = next(iter(today.values()))["exchangedate"]
        prev_date = datetime.strptime(date_str, "%d.%m.%Y") - timedelta(days=1)
        prev = get_rates(CURRENCIES, prev_date.strftime("%Y%m%d"))
    except requests.RequestException as e:
        print("Не удалось получить курсы:", e)
        sys.exit(1)

    existing = load_existing()
    rows = []
    for cc in CURRENCIES:
        if (date_str, cc) in existing:
            print(date_str, cc, "уже записан, пропускаю")
            continue
        rate = today[cc]["rate"]
        change = round(rate - prev[cc]["rate"], 4) if cc in prev else ""
        rows.append([date_str, cc, rate, change])
        print(date_str, cc, rate, "изменение:", change)

    if rows:
        save_rows(rows)
        print("Сохранено строк:", len(rows))
    else:
        print("Новых данных нет")


if __name__ == "__main__":
    main()