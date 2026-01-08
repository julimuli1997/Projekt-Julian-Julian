from Datenbank import get_connection #Stellt die Verbindung zur Datenbank her
from Datenbank import execute #Importiert die allgemeine SQL-Funktion
import os
import csv
import json
from decimal import Decimal
from exporter import export_all_to_csv, export_all_to_json, export_pc_config_to_csv, import_from_csv, import_from_json


def insert(table, columns, values): #Fügt einen neuen Eintrag in die Tabelle ein oder aktualisiert ihn bei Duplikat:
    placeholders = ','.join(['%s'] * len(values)) 
    cols = ','.join(columns)
    updates = ','.join([f"{col}=VALUES({col})" for col in columns if col != "id"])
    execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}", values)

def export(table, search_term=None): #Exportiert alle Einträge aus der angegebenen Tabelle:
    if search_term:
        # Fügt %-Wildcards für eine LIKE-Suche hinzu
        query = f"SELECT * FROM {table} WHERE klarnamen LIKE %s"
        params = (f"%{search_term}%",)
        return execute(query, params, fetch=True)
    else:
        return execute(f"SELECT * FROM {table}", fetch=True)

fetch_table = export # Alias für die GUI

def update(table, key_column, key_value, updates: dict): #Aktualisiert einen Eintrag in der Tabelle:
    set_clause = ", ".join([f"{k}=%s" for k in updates]) 
    values = tuple(updates.values()) + (key_value,)
    execute(f"UPDATE {table} SET {set_clause} WHERE {key_column}=%s", values)

def delete(table, key_column, key_value): #Löscht einen Eintrag aus der Tabelle:
    execute(f"DELETE FROM {table} WHERE {key_column}=%s", (key_value,))


columns_map = {
    "cases": ["seriennummer","klarnamen","groesse","farbe","status","preis"],
    "grafikkarten": ["seriennummer","klarnamen","groesse","status","preis"],
    "prozessoren": ["seriennummer","klarnamen","status","preis"],
    "mainboards": ["seriennummer","klarnamen","groesse","status","preis"],
    "arbeitsspeicher": ["seriennummer","klarnamen","speichergroesse","status","preis"],
    "festplatten": ["seriennummer","klarnamen","speichergroesse","status","preis"],
    "netzteile": ["seriennummer","klarnamen","leistung","status","preis"],
    "kuehler": ["seriennummer","klarnamen","typ","status","preis"],
    "zubehoer": ["seriennummer","klarnamen","typ","status","preis"]
}

def add_product(table_name, data):
    """Fügt ein neues Produkt in die angegebene Tabelle ein."""
    if table_name not in columns_map:
        raise ValueError(f"Unbekannte Tabelle: {table_name}")

    columns = columns_map[table_name]
    values = [data.get(col) for col in columns]
    insert(table_name, columns, values)
    print(f"Produkt in '{table_name}' hinzugefügt: {data}")


# -------------------------------
# Beispiel-Daten einfügen
# -------------------------------

def fill_all():
    tables_data = {
        "cases": [ #4 Beispiel-Einträge für Cases
            ("CASE001","NZXT H510","ATX","Schwarz","Verfügbar",89.99), 
            ("CASE002","Corsair 4000D","ATX","Weiß","Verfügbar",79.99),
            ("CASE003","Meshify C","ATX","Schwarz","Verfügbar",99.99),
            ("CASE004","MasterBox","ATX","Blau","Verfügbar",69.99)
        ],
        "grafikkarten": [ #4 Beispiel-Einträge für Grafikkarten
            ("GPU001","RTX 4070","Groß","Verfügbar",649.99),
            ("GPU002","RTX 4080","Groß","Verfügbar",1199.99),
            ("GPU003","RX 7900 XT","Groß","Verfügbar",899.99),
            ("GPU004","GTX 1660","Mittel","Verfügbar",249.99)
        ],
        "prozessoren": [ #4 Beispiel-Einträge für Prozessoren
            ("CPU001","Intel i7-12700K","Verfügbar",399.99),
            ("CPU002","Intel i9-12900K","Verfügbar",599.99),
            ("CPU003","Ryzen 7 5800X","Verfügbar",349.99),
            ("CPU004","Ryzen 9 5900X","Verfügbar",499.99)
        ],
        "mainboards": [ #4 Beispiel-Einträge für Mainboards
            ("MB001","ASUS B660","ATX","Verfügbar",219.99),
            ("MB002","MSI B550","ATX","Verfügbar",189.99),
            ("MB003","Gigabyte Z690","ATX","Verfügbar",299.99),
            ("MB004","ASRock B660","ATX","Verfügbar",179.99)
        ],
        "arbeitsspeicher": [ #4 Beispiel-Einträge für Arbeitsspeicher
            ("RAM001","Corsair Vengeance","16GB","Verfügbar",79.99),
            ("RAM002","G.Skill Trident Z","32GB","Verfügbar",159.99),
            ("RAM003","Kingston Fury","16GB","Verfügbar",89.99),
            ("RAM004","Crucial Ballistix","32GB","Verfügbar",149.99)
        ],
        "festplatten": [ #4 Beispiel-Einträge für Festplatten
            ("HDD001","Samsung 970 EVO","1TB","Verfügbar",109.99),
            ("HDD002","WD Blue SN550","1TB","Verfügbar",89.99),
            ("HDD003","Crucial MX500","500GB","Verfügbar",59.99),
            ("HDD004","Seagate Barracuda","2TB","Verfügbar",79.99)
        ],
        "netzteile": [ #4 Beispiel-Einträge für Netzteile
            ("PSU001","Corsair RM750","750W","Verfügbar",129.99),
            ("PSU002","Seasonic GX650","650W","Verfügbar",119.99),
            ("PSU003","BeQuiet 750W","750W","Verfügbar",139.99),
            ("PSU004","Cooler Master 650W","650W","Verfügbar",99.99)
        ],
        "kuehler": [ #4 Beispiel-Einträge für Kühler
            ("COOL001","Noctua NH-D15","Luft","Verfügbar",89.99),
            ("COOL002","Dark Rock Pro 4","Luft","Verfügbar",79.99),
            ("COOL003","Corsair H100i","Wasser","Verfügbar",119.99),
            ("COOL004","NZXT Kraken X63","Wasser","Verfügbar",129.99)
        ],
        "zubehoer": [ #4 Beispiel-Einträge für Zubehör
            ("ZUB001","RGB-Strip","Beleuchtung","Verfügbar",29.99),
            ("ZUB002","Mauspad XXL","Peripherie","Verfügbar",19.99),
            ("ZUB003","Gaming-Tastatur","Peripherie","Verfügbar",49.99),
            ("ZUB004","Monitorarm","Zubehör","Verfügbar",39.99)
        ]
    }

    # Spalten für jede Tabelle
    

    # Alle Tabellen optional leeren vor Einfügen
    for table in tables_data.keys():
        execute(f"DELETE FROM {table}") #Löscht alle Einträge in der Tabelle
        execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1") #Setzt Auto-Increment zurück

    # Einfügen
    for table, rows in tables_data.items():
        cols = columns_map[table]
        for row in rows:
            insert(table, cols, row)

# Erfolgsmeldung
    print("✅ Alle Tabellen wurden sauber mit 4 Einträgen gefüllt, keine Duplikate!")

#Funktionen zum Anzeigen der Daten

def show_all():
    tables = {
        "cases": "cases",
        "grafikkarten": "grafikkarten",
        "prozessoren": "prozessoren",
        "mainboards": "mainboards",
        "arbeitsspeicher": "arbeitsspeicher",
        "festplatten": "festplatten",
        "netzteile": "netzteile",
        "kuehler": "kuehler",
        "zubehoer": "zubehoer"
        }
    for name, table in tables.items():
        print(f"\n--- {name} ---")
        data = export(table)
        if data:
            for row in data:
                print(row)

def make_pc_config(filename="pc_konfiguration.json", selection=None):
    # Standard-Konfiguration, falls keine Auswahl übergeben wird
    if selection is None:
        selection = {
            "cases": "CASE001",
            "prozessoren": "CPU001",
            "grafikkarten": "GPU001",
            "mainboards": "MB001",
            "arbeitsspeicher": "RAM001",
            "festplatten": "HDD001",
            "netzteile": "PSU001",
            "kuehler": "COOL001"
        }

    pc_list = []
    for table, serial in selection.items():
        # Holt das Bauteil anhand der Seriennummer aus der jeweiligen Tabelle
        result = execute(f"SELECT * FROM {table} WHERE seriennummer=%s", (serial,), fetch=True)
        if result:
            pc_list.append(result[0])

    # Speichert die zusammengestellte Liste als JSON-Datei
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(pc_list, f, indent=4, ensure_ascii=False)
    print(f"PC-Konfiguration wurde erfolgreich in '{filename}' gespeichert.")

    
if __name__ == "__main__":
    fill_all()
    export_all_to_csv()
    export_all_to_json()
    import_from_csv("kuehler", "export/kuehler1.csv")
    import_from_json("cases", "export/cases1.json")