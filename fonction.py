import json
import calendar
from datetime import date

def load_json_file(file_path):     
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def choose_date():
    annee, mois = 2026, 8

    dernier_jour =  calendar.monthrange(annee, mois)[1]

    debut_mois = date(annee, mois, 1)
    fin_mois = date(annee, mois, dernier_jour)

    return debut_mois, fin_mois



