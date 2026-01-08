import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                               QHBoxLayout, QWidget, QLineEdit, QFormLayout, 
                               QComboBox, QLabel, QGroupBox, QTabWidget, QFrame)
from main import *

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnifiedWindow()
    window.show()
    sys.exit(app.exec())