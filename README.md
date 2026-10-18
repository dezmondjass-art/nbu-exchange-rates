# NBU Exchange Rates Tracker

A small Python script that collects official exchange rates from the
National Bank of Ukraine (NBU) API, calculates the daily change and
saves the history to a CSV file.

## Features

- Fetches USD, EUR and PLN rates (the list is easy to change)
- Calculates the change compared to the previous day
- Appends results to `rates.csv` without creating duplicates
- Handles network errors with a clear message and a non-zero exit code

## Installation

    python -m venv venv
    venv\Scripts\activate
    python -m pip install -r requirements.txt

## Usage

    python rates.py

## Example output

    19.10.2026 USD 44.8625 change: -0.0246
    19.10.2026 EUR 50.4977 change: 0.1896
    19.10.2026 PLN 11.5573 change: 0.0432

## Data source

NBU open API: https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange

## Daily automation (Windows)

The script can run every day via Windows Task Scheduler:

    schtasks /Create /SC DAILY /ST 18:00 /TN "NBU Rates" /TR "cmd /c cd /d C:\path\to\project && venv\Scripts\python.exe rates.py"

Replace `C:\path\to\project` with the folder where the project is located.