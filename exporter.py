import os
import csv
import json
from decimal import Decimal
from Datenbank import execute


# -------------------------------
# Hilfsfunktionen
# -------------------------------

def convert_decimals(rows):

#    Wandelt Decimal-Werte in float um (für JSON)

    for row in rows:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = float(value)
    return rows


def fetch_table(table_name):

#    Holt alle Daten aus einer Tabelle

    return execute(f"SELECT * FROM {table_name}", fetch=True)


# -------------------------------
# JSON Export
# -------------------------------

def export_to_json(table_name, folder="export"):

#    Exportiert eine Tabelle als JSON in den Export-Ordner

    os.makedirs(folder, exist_ok=True)

    filename = f"{table_name}.json"
    filepath = os.path.join(folder, filename)

    rows = fetch_table(table_name)

    if not rows:
        print(f"⚠️ Tabelle '{table_name}' ist leer – kein JSON-Export.")
        return

    rows = convert_decimals(rows)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)

    print(f"✅ {table_name} → {filepath}")


def export_all_to_json(folder="export"):
    tables = [
        "cases", "grafikkarten", "prozessoren", "mainboards",
        "arbeitsspeicher", "festplatten", "netzteile",
        "kuehler", "zubehoer", "pc_builds"
    ]

    for table in tables:
        export_to_json(table, folder)


# -------------------------------
# CSV Export
# -------------------------------

def export_to_csv(table_name, folder="export"):

#    Exportiert eine Tabelle als CSV

    os.makedirs(folder, exist_ok=True)

    filename = f"{table_name}.csv"
    filepath = os.path.join(folder, filename)

    rows = fetch_table(table_name)

    if not rows:
        print(f"⚠️ Tabelle '{table_name}' ist leer – kein CSV-Export.")
        return

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ {table_name} → {filepath}")


def export_all_to_csv(folder="export"):
    tables = [
        "cases", "grafikkarten", "prozessoren", "mainboards",
        "arbeitsspeicher", "festplatten", "netzteile",
        "kuehler", "zubehoer", "pc_builds"
    ]

    for table in tables:
       export_to_csv(table, folder)


# -------------------------------
# Testlauf
# -------------------------------

if __name__ == "__main__":
    export_all_to_csv()
    export_all_to_json()