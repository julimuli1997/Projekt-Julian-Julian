import sys
import os
import PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
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
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()
        self.setLayout(layout)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

