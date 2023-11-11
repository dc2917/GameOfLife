from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class HelpWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Documentation")
        browser = QWebEngineView()
        browser.load(QUrl("file:///home/dan/Documents/Python/GameOfLife/Qt/docs/build/html/index.html"))
        layout = QVBoxLayout()
        layout.addWidget(browser)
        self.setLayout(layout)
