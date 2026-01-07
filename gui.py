import sys
import os
import PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QFormLayout, QComboBox, QLabel, QGroupBox
from pathlib import Path


# Force the app to look in the exact spot you found earlier
# We use Path to make it robust against typos
site_packages = Path(sys.prefix) / "lib" / "python3.12" / "site-packages"
plugin_path = site_packages / "PySide6" / "Qt" / "plugins"

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(plugin_path)

print(f"Forcing plugin path to: {plugin_path}") # Debug print


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC-Shop")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #e0e0e0;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.search_database(layout)
        self.Pc_config_button(layout)
        layout.addStretch()

    # Mainwindow ist das Hauptmenü -> von hieraus gelangt man in alle anderen Fenster

    def search_database(self, layout):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Suche...")
        layout.addWidget(self.search_bar)
    
    def Pc_config_button(self, layout):
        self.pc_config_button = QPushButton("PC-Konfiguration erstellen")
        layout.addWidget(self.pc_config_button)
        self.pc_config_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.pc_config_button.clicked.connect(self.open_pc_config_window)

    def open_pc_config_window(self):
        self.pc_config_window = PcConfigWindow()
        self.pc_config_window.show()

    

class PcConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC-Konfiguration erstellen")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #e0e0e0;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # UI für den Konfigurator aufbauen
        self.setup_configurator_ui(layout)
        
        # Export Button ganz unten
        self.csv_export_button(layout)
        layout.addStretch() # Schiebt alles nach oben

    def csv_export_button(self, layout):
        self.export_btn = QPushButton("CSV-Export erstellen")
        layout.addWidget(self.export_btn)
        self.export_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")

    def setup_configurator_ui(self, layout):
        # Eine Gruppe für die Komponenten erstellen
        group_box = QGroupBox("Hardware Komponenten")
        group_box.setStyleSheet("""
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
            QLabel {
                color: black;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                background-color: #f9f9f9;
                color: black;
            }
            QComboBox:hover {
                border: 1px solid #3498db;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #3498db;
                selection-color: white;
                border: 1px solid #cccccc;
                outline: 0;
                color: black;
            }""")

        form_layout = QFormLayout()

        # Dropdowns (ComboBox) für die Teile
        self.cpu_combo = QComboBox()

        
        self.gpu_combo = QComboBox()


        self.ram_combo = QComboBox()
       

        # Dem Formular hinzufügen
        form_layout.addRow("Prozessor (CPU):", self.cpu_combo)
        form_layout.addRow("Grafikkarte (GPU):", self.gpu_combo)
        form_layout.addRow("Arbeitsspeicher (RAM):", self.ram_combo)

        group_box.setLayout(form_layout)
        layout.addWidget(group_box)

        # Preisanzeige
        self.price_label = QLabel("Gesamtpreis: 0,00 €")
        self.price_label.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 5px; margin-top: 10px;")
        layout.addWidget(self.price_label)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
