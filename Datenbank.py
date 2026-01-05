import mysql.connector
from mysql.connector import Error
import getpass

root_password = getpass.getpass("Enter MySQL root password: ")

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=root_password)
    
    cursor = connection.cursor()
    print("Connection to MySQL database established successfully.")

    cursor.execute("CREATE USER IF NOT EXISTS 'pcshop_user'@'localhost' IDENTIFIED BY 'xQrYP2ttqX*w5%P';")
    cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'pcshop_user'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")
    cursor.execute("CREATE DATABASE IF NOT EXISTS projekt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("Database 'projekt' created or already exists.")
    print("User erstellt und Rechte vergeben")
    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='pcshop_user',
        password='xQrYP2ttqX*w5%P',
        database='projekt'
    )

def execute(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def create_tables():
    conn = get_connection()

    # Cases
    execute(conn, """
    CREATE TABLE IF NOT EXISTS cases (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        groesse VARCHAR(20),
        farbe VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)
    # Grafikkarten
    execute(conn, """
    CREATE TABLE IF NOT EXISTS grafikkarten (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        groesse VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)

    # Prozessoren
    execute(conn, """
    CREATE TABLE IF NOT EXISTS prozessoren (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)

    # Mainboards
    execute(conn, """
    CREATE TABLE IF NOT EXISTS mainboards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        groesse VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)
    # Arbeitsspeicher
    execute(conn, """
    CREATE TABLE IF NOT EXISTS arbeitsspeicher (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        speichergroesse VARCHAR(30),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)
    #Festplatten
    execute(conn, """
    CREATE TABLE IF NOT EXISTS festplatten (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        speichergroesse VARCHAR(30),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)

    #Netzteile
    execute(conn, """
    CREATE TABLE IF NOT EXISTS netzteile (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        leistung VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)

    #Kühler
    execute(conn, """
    CREATE TABLE IF NOT EXISTS kuehler (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        typ VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)

    #Zubehör
    execute(conn, """
    CREATE TABLE IF NOT EXISTS zubehoer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        typ VARCHAR(30) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)

    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()