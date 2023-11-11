from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class HelpWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Documentation")
        docs_path = Path("./docs/build/html/index.html")
        browser = QWebEngineView()
        browser.load(QUrl(f"file://{Path(__file__).parent}/{docs_path}"))
        layout = QVBoxLayout()
        layout.addWidget(browser)
        self.setLayout(layout)
