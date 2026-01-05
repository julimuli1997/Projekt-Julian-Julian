import mysql.connector
from mysql.connector import Error

def get_connection(): #Stzellt die Verbindung zur Datenbank her:
    return mysql.connector.connect( #Verbindungsparameter zur Datenbank
        host='92.117.125.124', #Datenbank-Host
        user="admin", #Datenbank-Benutzername
        password="xQrYP2ttqX*w5%P", #Datenbank-Passwort
        database="projekt" #Datenbank-Name
    )

def execute(query, params=None, fetch=False): #Führt eine SQL-Abfrage aus:
    conn = get_connection() #Verbindung zur Datenbank herstellen
    cursor = conn.cursor(dictionary=True) #Cursor erstellen

    cursor.execute(query, params) #SQL-Abfrage ausführen

    result = cursor.fetchall() if fetch else None #Ergebnisse abrufen, falls erforderlich

    conn.commit() #Änderungen in der Datenbank speichern
    cursor.close() #Cursor schließen
    conn.close() #Verbindung zur Datenbank schließen
    return result #Ergebnisse zurückgeben


# Tabellen erstellen, falls sie nicht existieren
def create_tables():
    # CASES
    execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        groesse VARCHAR(20) NOT NULL,
        farbe VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # GRAFIKKARTEN
    execute("""
    CREATE TABLE IF NOT EXISTS grafikkarten (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        groesse VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # PROZESSOREN
    execute("""
    CREATE TABLE IF NOT EXISTS prozessoren (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # MAINBOARDS
    execute("""
    CREATE TABLE IF NOT EXISTS mainboards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        groesse VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # ARBEITSSPEICHER
    execute("""
    CREATE TABLE IF NOT EXISTS arbeitsspeicher (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        speichergroesse VARCHAR(30) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # FESTPLATTEN
    execute("""
    CREATE TABLE IF NOT EXISTS festplatten (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        speichergroesse VARCHAR(30) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # NETZTEILE
    execute("""
    CREATE TABLE IF NOT EXISTS netzteile (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        leistung VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # KÜHLER
    execute("""
    CREATE TABLE IF NOT EXISTS kuehler (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        typ VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    # ZUBEHÖR
    execute("""
    CREATE TABLE IF NOT EXISTS zubehoer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        typ VARCHAR(20) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    print("✅ Alle Tabellen wurden erfolgreich erstellt!")

if __name__ == "__main__":
    create_tables()