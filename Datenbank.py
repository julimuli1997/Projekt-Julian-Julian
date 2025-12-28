import mysql.connector
from mysql.connector import Error

def get_connection(): #Stzellt die Verbindung zur Datenbank her:
    return mysql.connector.connect( #Verbindungsparameter zur Datenbank
        host='localhost', #Datenbank-Host
        user="root", #Datenbank-Benutzername
        password="RBeCS$oiQ8s9RUo", #Datenbank-Passwort
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


