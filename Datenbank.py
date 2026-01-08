import mysql.connector
from mysql.connector import Error
import getpass

def initial_setup():
    """Führt das erstmalige Setup der Datenbank durch."""
    try:
        root_password = getpass.getpass("Enter MySQL root password: ")
        
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
        
        # Nach dem Setup direkt die Tabellen erstellen
        create_tables()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='pcshop_user',
        password='xQrYP2ttqX*w5%P',
        database='projekt'
    )

def execute(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    cursor.close()
    conn.close()
    return result


def create_tables():
    conn = get_connection()

    # Cases
    execute("""
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
    execute("""
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
    execute("""
    CREATE TABLE IF NOT EXISTS prozessoren (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50),
        klarnamen VARCHAR(20),
        status ENUM('Verfügbar','Ausverkauft'),
        preis DECIMAL(10,2)
    )
    """)

    # Mainboards
    execute("""
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
    execute("""
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
    execute("""
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
    execute("""
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
    execute("""
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
    execute("""
    CREATE TABLE IF NOT EXISTS zubehoer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        seriennummer VARCHAR(50) NOT NULL UNIQUE,
        klarnamen VARCHAR(20) NOT NULL,
        typ VARCHAR(30) NOT NULL,
        status ENUM('Verfügbar','Ausverkauft') NOT NULL,
        preis DECIMAL(10,2) NOT NULL
    )
    """)
    #PC Builds
    execute("""
    CREATE TABLE IF NOT EXISTS pc_builds(
            id INT AUTO_INCREMENT PRIMARY KEY,
            
            case_id INT NOT NULL,
            grafikkarte_id INT NOT NULL,
            prozessor_id INT NOT NULL,
            mainboard_id INT NOT NULL,
            arbeitsspeicher_id INT NOT NULL,
            festplatte_id INT NOT NULL,
            netzteil_id INT NOT NULL,
            kuehler_id INT NOT NULL,
            zubehoer_id INT NOT NULL,
            
            CONSTRAINT fk_case FOREIGN KEY (case_id) 
            REFERENCES cases(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_grafikkarte FOREIGN KEY (grafikkarte_id) 
            REFERENCES grafikkarten(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_prozessor FOREIGN KEY (prozessor_id) 
            REFERENCES prozessoren(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_mainboard FOREIGN KEY (mainboard_id) 
            REFERENCES mainboards(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_arbeitsspeicher FOREIGN KEY (arbeitsspeicher_id) 
            REFERENCES arbeitsspeicher(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_festplatte FOREIGN KEY (festplatte_id) 
            REFERENCES festplatten(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_netzteil FOREIGN KEY (netzteil_id) 
            REFERENCES netzteile(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_kuehler FOREIGN KEY (kuehler_id) 
            REFERENCES kuehler(id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_zubehoer FOREIGN KEY (zubehoer_id) 
            REFERENCES zubehoer(id)
            ON DELETE RESTRICT ON UPDATE CASCADE
    )
    """)


    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    initial_setup()