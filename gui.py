import sys
import os
import PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QTableWidget, QTableWidgetItem
from main import *

#Initiallisiert dsa Main-Window der Anwendung
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC-Shop")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        # Tab-Widget erstellen und zum Layout hinzufügen
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Tabs initialisieren
        self.tab_PC_Teile()
        self.export_to_csv_button()

    def tab_PC_Teile(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Unter-Tabs für die verschiedenen Kategorien
        sub_tabs = QTabWidget()
        categories = ["cases", "grafikkarten", "prozessoren", "mainboards", 
                      "arbeitsspeicher", "festplatten", "netzteile", "kuehler", "zubehoer"]
        
        for category in categories:
            table = QTableWidget()
            data = export(category) # Daten aus der Datenbank holen
            if data:
                headers = list(data[0].keys())
                table.setColumnCount(len(headers))
                table.setHorizontalHeaderLabels(headers)
                table.setRowCount(len(data))
                for i, row in enumerate(data):
                    for j, key in enumerate(headers):
                        table.setItem(i, j, QTableWidgetItem(str(row[key])))
            sub_tabs.addTab(table, category.capitalize())
            
        layout.addWidget(sub_tabs)
        self.tabs.addTab(tab, "PC Teile")


#Button für CSV Export auf Mainpage
    def export_to_csv_button(self):
        button = QPushButton("CSV Export")
        button.setStyleSheet("background-color: black; color: white;")
        button.clicked.connect(export_to_csv)
        self.layout.addWidget(button)





app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
