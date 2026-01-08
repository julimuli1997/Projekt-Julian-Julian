import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                               QHBoxLayout, QWidget, QLineEdit, QFormLayout, 
                               QComboBox, QLabel, QGroupBox, QTabWidget, QFrame,
                               QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtGui import QColor
from main import *
from exporter import *
from Datenbank import *



# Plugin Path Fix (aus deinem Originalcode)
site_packages = Path(sys.prefix) / "lib" / "python3.12" / "site-packages"
plugin_path = site_packages / "PySide6" / "Qt" / "plugins"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(plugin_path)


# ---------------------------------------------------------
# 1. LINKER OBERER BEREICH: Menü
# ---------------------------------------------------------
class MenuPanel(QFrame):
    def __init__(self):
        super().__init__()
        # Styling: Hellgrau, keine abgerundeten Ecken mehr für nahtlosen Look
        self.setStyleSheet("background-color: #e0e0e0; border-bottom: 1px solid #cccccc;")
        
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("PC-Shop (Menü)")
        title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        layout.addWidget(title)

        # Suche
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Suche...")
        layout.addWidget(self.search_bar)

        # Buttons
        self.pc_config_button = QPushButton("PC-Konfiguration zurücksetzen")
        self.pc_config_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.pc_config_button)

        self.all_products_button = QPushButton("Produkte aktualisieren")
        self.all_products_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.all_products_button)

        layout.addStretch()


# ---------------------------------------------------------
# 2. LINKER UNTERER BEREICH: Konfigurator
# ---------------------------------------------------------
class ConfigPanel(QFrame):
    def __init__(self):
        super().__init__()
        # Styling: Hellgrau
        self.setStyleSheet("background-color: #e0e0e0;")

        # Cache für Komponentendaten
        self.component_data = {}

        layout = QVBoxLayout(self)

        title = QLabel("PC-Konfiguration erstellen")
        title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Styles für die Boxen
        group_box_style = """
            QGroupBox {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 15px; 
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #333333;
                font-weight: bold;
            }
            QLabel { color: black; }
            QComboBox { color: black; }
        """

        group_box = QGroupBox("Hardware Komponenten")
        group_box.setStyleSheet(group_box_style)

        form_layout = QFormLayout()
        self.case_combo = QComboBox()
        self.gpu_combo = QComboBox()
        self.cpu_combo = QComboBox()
        self.mainboard_combo = QComboBox()
        self.ram_combo = QComboBox()
        self.disk_combo = QComboBox()
        self.psu_combo = QComboBox()
        self.cooler_combo = QComboBox()
        self.accessory_combo = QComboBox()

        # Alle Comboboxen für die Iteration sammeln
        self.combos = [
            self.case_combo, self.gpu_combo, self.cpu_combo, self.mainboard_combo,
            self.ram_combo, self.disk_combo, self.psu_combo, self.cooler_combo,
            self.accessory_combo
        ]

        form_layout.addRow("Cases:", self.case_combo)
        form_layout.addRow("Grafikkarten:", self.gpu_combo)
        form_layout.addRow("Prozessoren:", self.cpu_combo)
        form_layout.addRow("Mainboards:", self.mainboard_combo)
        form_layout.addRow("Arbeitsspeicher:", self.ram_combo)
        form_layout.addRow("Festplatten:", self.disk_combo)
        form_layout.addRow("Netzteile:", self.psu_combo)
        form_layout.addRow("Kühler:", self.cooler_combo)
        form_layout.addRow("Zubehör:", self.accessory_combo)

        group_box.setLayout(form_layout)
        layout.addWidget(group_box)

        # Preis
        self.price_label = QLabel("Gesamtpreis: 0,00 €")
        self.price_label.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 5px; margin-top: 10px;")
        layout.addWidget(self.price_label)

        layout.addStretch()

        self.export_btn = QPushButton("CSV-Export erstellen")
        self.export_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.export_btn)

        # Signale verbinden
        for combo in self.combos:
            combo.currentIndexChanged.connect(self.calculate_total_price)
    
    def fill_in_dropdowns_from_db(self):
        """Füllt die Dropdown-Menüs mit Daten aus der Datenbank und cacht diese."""
        self.component_data.clear() # Cache leeren
        
        combo_map = {
            self.case_combo: "cases",
            self.gpu_combo: "grafikkarten",
            self.cpu_combo: "prozessoren",
            self.mainboard_combo: "mainboards",
            self.ram_combo: "arbeitsspeicher",
            self.disk_combo: "festplatten",
            self.psu_combo: "netzteile",
            self.cooler_combo: "kuehler",
            self.accessory_combo: "zubehoer"
        }

        for combo, table_name in combo_map.items():
            combo.clear()
            combo.addItem("")  # Fügt ein leeres Element hinzu
            try:
                data = fetch_table(table_name)
                self.component_data[table_name] = data # Daten im Cache speichern
                if data:
                    for item in data:
                        combo.addItem(item.get("klarnamen", "N/A"))
            except Exception as e:
                print(f"Fehler beim Laden von Dropdown-Daten für {table_name}: {e}")
                combo.addItem("Laden fehlgeschlagen")
        
        self.calculate_total_price() # Preis initial berechnen

    def calculate_total_price(self):
        """Berechnet den Gesamtpreis der ausgewählten Komponenten."""
        total = Decimal("0.00")
        
        combo_map = {
            self.case_combo: "cases",
            self.gpu_combo: "grafikkarten",
            self.cpu_combo: "prozessoren",
            self.mainboard_combo: "mainboards",
            self.ram_combo: "arbeitsspeicher",
            self.disk_combo: "festplatten",
            self.psu_combo: "netzteile",
            self.cooler_combo: "kuehler",
            self.accessory_combo: "zubehoer"
        }

        for combo, table_name in combo_map.items():
            selected_name = combo.currentText()
            if selected_name and table_name in self.component_data:
                # Finde das passende Item im Cache
                for item in self.component_data[table_name]:
                    if item.get("klarnamen") == selected_name:
                        total += Decimal(item.get("preis", "0.00"))
                        break
        
        self.price_label.setText(f"Gesamtpreis: {total:.2f} €")


# ---------------------------------------------------------
# 3. RECHTER BEREICH: Produktliste
# ---------------------------------------------------------
class ProductListPanel(QFrame):
    def __init__(self):
        super().__init__()
        # Styling: Hellgrau, linker Rand als Trennlinie
        self.setStyleSheet("background-color: #e0e0e0; border-left: 1px solid #cccccc;")

        layout = QVBoxLayout(self)

        title = QLabel("Alle Produkte anzeigen")
        title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()
        categories = ["Cases", "Grafikkarten", "Prozessoren", "Mainboards", 
                      "Arbeitsspeicher", "Festplatten", "Netzteile", "Kühler", "Zubehör"]

        for category in categories:
            tab = QWidget()
            self.tabs.addTab(tab, category)

        self.tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #C2C7CB; background: white; } QTabBar::tab { color: black; }")
        layout.addWidget(self.tabs)

        # Buttons
        button_layout = QHBoxLayout()
        self.export_btn = QPushButton("CSV-Export erstellen")
        self.export_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.export_btn)
        
        self.add_product_btn = QPushButton("Produkt hinzufügen")
        self.add_product_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.add_product_btn)

        layout.addLayout(button_layout)

    def populate_tabs(self):
        """Füllt die Tabs mit Daten aus der Datenbank."""
        # Zuordnung von Tab-Namen zu Datenbank-Tabellen
        tab_map = {
            "Cases": "cases",
            "Grafikkarten": "grafikkarten",
            "Prozessoren": "prozessoren",
            "Mainboards": "mainboards",
            "Arbeitsspeicher": "arbeitsspeicher",
            "Festplatten": "festplatten",
            "Netzteile": "netzteile",
            "Kühler": "kuehler",
            "Zubehör": "zubehoer"
        }

        for i in range(self.tabs.count()):
            category = self.tabs.tabText(i)
            table_name = tab_map.get(category)
            
            if not table_name:
                continue

            # Das Widget des aktuellen Tabs holen
            tab_widget = self.tabs.widget(i)
            
            # Layout erstellen oder bestehendes bereinigen (falls Refresh geklickt wird)
            if not tab_widget.layout():
                layout = QVBoxLayout(tab_widget)
            else:
                layout = tab_widget.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            
            # Daten aus der DB holen
            try:
                data = fetch_table(table_name)
            except Exception as e:
                print(f"Fehler beim Laden von {table_name}: {e}")
                data = []
            
            if not data:
                layout.addWidget(QLabel("Keine Daten verfügbar."))
                continue

            # Tabelle erstellen und konfigurieren
            table_widget = QTableWidget()
            headers = list(data[0].keys())
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(data))
            
            # Vertikale Kopfzeile (Nummerierung) ausblenden
            table_widget.verticalHeader().setVisible(False)

            # Horizontale Kopfzeile (Spaltentitel) konfigurieren
            header_view = table_widget.horizontalHeader()
            header_view.setSectionResizeMode(QHeaderView.Stretch)
            header_view.setStyleSheet("::section { color: black; }")
            
            # Daten in die Tabelle füllen
            for row_idx, row_data in enumerate(data):
                for col_idx, header in enumerate(headers):
                    val = row_data.get(header, "")
                    item = QTableWidgetItem(str(val))
                    item.setForeground(QColor("black")) # Schriftfarbe auf Schwarz setzen
                    table_widget.setItem(row_idx, col_idx, item)
            
            layout.addWidget(table_widget)


# ---------------------------------------------------------
# HAUPTFENSTER
# ---------------------------------------------------------
class UnifiedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC-Shop Dashboard")
        self.setGeometry(100, 100, 1200, 700)
        
        # WICHTIG: Keine dunkle Hintergrundfarbe mehr setzen!
        # Standard-Grau belassen, damit keine schwarzen Balken entstehen.

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Hauptlayout
        main_h_layout = QHBoxLayout(central_widget)
        # Alles auf 0, damit die Teile sich berühren
        main_h_layout.setSpacing(0)
        main_h_layout.setContentsMargins(0, 0, 0, 0)

        # --- LINKS ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(0) # Kein Abstand zwischen oben und unten
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_panel = MenuPanel()
        left_layout.addWidget(self.menu_panel, 1)

        self.config_panel = ConfigPanel()
        left_layout.addWidget(self.config_panel, 1)

        main_h_layout.addWidget(left_container, 1)

        # --- RECHTS ---
        self.product_panel = ProductListPanel()
        main_h_layout.addWidget(self.product_panel, 2)

        # Tabs und Dropdowns initial befüllen
        self.product_panel.populate_tabs()
        self.config_panel.fill_in_dropdowns_from_db()
        
        # Refresh-Button verbinden
        self.menu_panel.all_products_button.clicked.connect(self.product_panel.populate_tabs)
        self.menu_panel.all_products_button.clicked.connect(self.config_panel.fill_in_dropdowns_from_db)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fill_all()
    window = UnifiedWindow()
    window.show()
    sys.exit(app.exec())