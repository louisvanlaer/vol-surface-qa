import json
import calendar
from datetime import date
import pandas as pd

def load_json_file(file_path):
    try:     
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalid : {file_path}") from e

def get_request(path,trade_date,instrument):
    response = load_json_file(path)
    rows = response["data"]
    trade_date = sorted({
        row["trading_date"]
        for row in rows
    })

    instrument = sorted({
        row["RIC"]
        for row in rows
    })

    return trade_date, instrument

def choose_date():
    annee, mois = 2026, 8

    dernier_jour =  calendar.monthrange(annee, mois)[1]

    debut_mois = date(annee, mois, 1)
    fin_mois = date(annee, mois, dernier_jour)

    return debut_mois, fin_mois





