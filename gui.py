import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QListWidget)
from PySide6.QtCore import Qt

class MySimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Window Setup
        self.setWindowTitle("Quick Note Planner")
        self.resize(400, 500)

        # 2. Create the Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 3. Add UI Elements (Widgets)
        self.label = QLabel("Enter your task below:")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something here...")

        self.add_button = QPushButton("Add to List")
        self.note_list = QListWidget()

        # 4. Add Widgets to Layout
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.add_button)
        layout.addWidget(self.note_list)

        # 5. Connect Signals (Events)
        self.add_button.clicked.connect(self.add_item_to_list)

    def add_item_to_list(self):
        text = self.input_field.text()
        if text.strip():
            self.note_list.addItem(text)
            self.input_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MySimpleApp()
    window.show()
    
    sys.exit(app.exec())
