import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                               QHBoxLayout, QWidget, QLineEdit, QFormLayout, 
                               QComboBox, QLabel, QGroupBox, QTabWidget, QFrame,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QDialog, QDialogButtonBox, QMessageBox, QFileDialog, QAbstractItemView)
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from decimal import Decimal
from main import fetch_table, add_product, columns_map, fill_all, export_pc_config_to_csv, delete
from exporter import import_from_csv, import_from_json




# Plugin Path Fix (aus deinem Originalcode)
site_packages = Path(sys.prefix) / "lib" / "python3.12" / "site-packages"
plugin_path = site_packages / "PySide6" / "Qt" / "plugins"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(plugin_path)


# ---------------------------------------------------------
# 1. LINKER OBERER BEREICH: Menü
# ---------------------------------------------------------
class MenuPanel(QFrame):
    data_imported = Signal()
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
        self.import_button = QPushButton("Daten importieren")
        self.import_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.import_button)

        self.pc_config_button = QPushButton("PC-Konfiguration zurücksetzen")
        self.pc_config_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.pc_config_button)

        self.all_products_button = QPushButton("Produkte aktualisieren")
        self.all_products_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.all_products_button)

        layout.addStretch()

        self.import_button.clicked.connect(self.handle_import_click)

    def handle_import_click(self):
        """Öffnet einen Dateidialog zum Importieren von CSV- oder JSON-Dateien."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Daten importieren",
            "", # Startverzeichnis
            "Daten-Dateien (*.csv *.json)"
        )

        if not filepath:
            return

        try:
            p = Path(filepath)
            table_name = p.stem.split('.')[0] # Extrahiert den Tabellennamen aus dem Dateinamen
            
            if p.suffix == ".csv":
                import_from_csv(table_name, filepath)
            elif p.suffix == ".json":
                import_from_json(table_name, filepath)
            else:
                QMessageBox.warning(self, "Fehler", "Nicht unterstützter Dateityp.")
                return

            QMessageBox.information(self, "Erfolg", f"Daten wurden erfolgreich in '{table_name}' importiert.")
            self.data_imported.emit() # Signal senden, um die UI zu aktualisieren

        except Exception as e:
            QMessageBox.critical(self, "Importfehler", f"Ein Fehler ist aufgetreten:\n{e}")




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
        self.export_btn.clicked.connect(self.handle_export_click)
    
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

    def handle_export_click(self):
        """Sammelt die ausgewählten Komponenten und exportiert sie als CSV."""
        selected_components = []
        
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
                        selected_components.append(item)
                        break
        
        if not selected_components:
            QMessageBox.warning(self, "Export fehlgeschlagen", "Es wurden keine Komponenten für die Konfiguration ausgewählt.")
            return

        # Exportfunktion aufrufen
        success, message = export_pc_config_to_csv(selected_components)

        if success:
            QMessageBox.information(self, "Export erfolgreich", f"Die PC-Konfiguration wurde erfolgreich exportiert nach:\n{message}")
        else:
            QMessageBox.critical(self, "Export fehlgeschlagen", f"Ein Fehler ist aufgetreten:\n{message}")



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

        # Signal verbinden
        self.add_product_btn.clicked.connect(self.open_add_product_dialog)


    def populate_tabs(self, search_term=None):
        """Füllt die Tabs mit Daten aus der Datenbank, optional gefiltert."""
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
            
            # Layout erstellen oder bestehendes bereinigen
            if not tab_widget.layout():
                layout = QVBoxLayout(tab_widget)
            else:
                layout = tab_widget.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            
            # Daten aus der DB holen, optional gefiltert
            try:
                data = fetch_table(table_name, search_term=search_term)
            except Exception as e:
                print(f"Fehler beim Laden von {table_name}: {e}")
                data = []
            
            if not data:
                layout.addWidget(QLabel("Keine Daten verfügbar."))
                continue

            # Tabelle erstellen und konfigurieren
            table_widget = QTableWidget()
            # Die Header aus der `columns_map` holen, um die korrekte Reihenfolge sicherzustellen
            headers = columns_map.get(table_name, list(data[0].keys()))
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
            
            table_widget.cellClicked.connect(self.handle_product_click)
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
            table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            layout.addWidget(table_widget)
    
    def open_add_product_dialog(self):
        """Öffnet den Dialog zum Hinzufügen eines neuen Produkts."""
        # Zuordnung von Tab-Namen zu Datenbank-Tabellen
        tab_map = {
            "Cases": "cases", "Grafikkarten": "grafikkarten", "Prozessoren": "prozessoren",
            "Mainboards": "mainboards", "Arbeitsspeicher": "arbeitsspeicher",
            "Festplatten": "festplatten", "Netzteile": "netzteile",
            "Kühler": "kuehler", "Zubehör": "zubehoer"
        }

        current_tab_text = self.tabs.tabText(self.tabs.currentIndex())
        table_name = tab_map.get(current_tab_text)

        if not table_name:
            QMessageBox.warning(self, "Fehler", "Keine gültige Kategorie ausgewählt.")
            return

        dialog = AddProductDialog(table_name, parent=self)
        if dialog.exec() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                add_product(table_name, data)
                QMessageBox.information(self, "Erfolg", f"Produkt wurde erfolgreich zu '{current_tab_text}' hinzugefügt.")
                self.populate_tabs() # Tabs neu laden
            except Exception as e:
                QMessageBox.critical(self, "Datenbankfehler", f"Fehler beim Hinzufügen des Produkts:\n{e}")

    def handle_product_click(self, row, column):
        """Löscht das ausgewählte Produkt aus der Datenbank."""
        # Aktuellen Tab und Tabelle ermitteln
        current_tab_widget = self.tabs.currentWidget()
        if not current_tab_widget or not hasattr(current_tab_widget, 'layout') or not current_tab_widget.layout():
            return

        table_widget = current_tab_widget.findChild(QTableWidget)
        if not table_widget:
            # This should not happen if the signal is connected correctly
            return

        # Annahme: Die erste Spalte ist die Seriennummer, aber wir suchen den Header
        headers = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
        try:
            sn_col_index = headers.index("seriennummer")
        except ValueError:
            QMessageBox.critical(self, "Fehler", "Die Spalte 'seriennummer' wurde nicht gefunden.")
            return

        serial_number_item = table_widget.item(row, sn_col_index)
        if not serial_number_item:
            return

        serial_number = serial_number_item.text()
        
        # Tabellennamen ermitteln
        tab_map = {
            "Cases": "cases", "Grafikkarten": "grafikkarten", "Prozessoren": "prozessoren",
            "Mainboards": "mainboards", "Arbeitsspeicher": "arbeitsspeicher",
            "Festplatten": "festplatten", "Netzteile": "netzteile",
            "Kühler": "kuehler", "Zubehör": "zubehoer"
        }
        current_tab_text = self.tabs.tabText(self.tabs.currentIndex())
        table_name = tab_map.get(current_tab_text)

        if not table_name:
            return

        # Bestätigungsdialog
        reply = QMessageBox.question(
            self,
            "Löschen bestätigen",
            f"Möchten Sie das Produkt mit der Seriennummer '{serial_number}' wirklich löschen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                delete(table_name, "seriennummer", serial_number)
                QMessageBox.information(self, "Erfolg", "Das Produkt wurde erfolgreich gelöscht.")
                
                # UI aktualisieren
                self.populate_tabs()
                
                # Das config_panel über das Hauptfenster aktualisieren
                main_window = self.parent().parent()
                if hasattr(main_window, 'config_panel'):
                    main_window.config_panel.fill_in_dropdowns_from_db()

            except Exception as e:
                QMessageBox.critical(self, "Datenbankfehler", f"Fehler beim Löschen des Produkts:\n{e}")


# ---------------------------------------------------------
# 4. DIALOG ZUM HINZUFÜGEN VON PRODUKTEN
# ---------------------------------------------------------
class AddProductDialog(QDialog):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Neues Produkt für '{table_name}' hinzufügen")
        self.setStyleSheet("""
            QDialog {
                background-color: white; 
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: black;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
        """)

        self.table_name = table_name
        self.input_widgets = {}

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Dynamisch Eingabefelder erstellen
        columns = columns_map.get(self.table_name, [])
        for col in columns:
            if col == "id": continue # ID wird automatisch vergeben

            label = QLabel(col.replace("_", " ").title() + ":")
            if col == "status":
                widget = QComboBox()
                widget.addItems(["Verfügbar", "Ausverkauft"])
            else:
                widget = QLineEdit()
            
            form_layout.addRow(label, widget)
            self.input_widgets[col] = widget

        layout.addLayout(form_layout)

        # OK/Cancel Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Styling für die Buttons
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")

        layout.addWidget(button_box)

    def get_data(self):
        """Sammelt die Daten aus den Eingabefeldern."""
        data = {}
        for col, widget in self.input_widgets.items():
            if isinstance(widget, QComboBox):
                data[col] = widget.currentText()
            else:
                data[col] = widget.text()
        return data


# ---------------------------------------------------------
# HAUPTFENSTER
# ---------------------------------------------------------
class UnifiedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC-Shop Dashboard")
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_h_layout = QHBoxLayout(central_widget)
        main_h_layout.setSpacing(0)
        main_h_layout.setContentsMargins(0, 0, 0, 0)

        # --- LINKS ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(0)
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
        
        # --- Signale verbinden ---
        # Suchleiste
        self.menu_panel.search_bar.textChanged.connect(self.handle_search)
        
        # "Produkte aktualisieren"-Button leert die Suche und füllt alles neu
        self.menu_panel.all_products_button.clicked.connect(
            lambda: self.menu_panel.search_bar.clear()
        )
        self.menu_panel.all_products_button.clicked.connect(
            self.config_panel.fill_in_dropdowns_from_db
        )

        # Signal für Datenimport verbinden
        self.menu_panel.data_imported.connect(self.product_panel.populate_tabs)
        self.menu_panel.data_imported.connect(self.config_panel.fill_in_dropdowns_from_db)

    def handle_search(self, text):
        """Wird aufgerufen, wenn sich der Text in der Suchleiste ändert."""
        self.product_panel.populate_tabs(search_term=text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fill_all()
    window = UnifiedWindow()
    window.show()
    sys.exit(app.exec())