"""Ponto de entrada do Sistema de Controle de Estoque."""

import sys

from PySide6.QtWidgets import QApplication, QStackedWidget

from views.login import LoginWindow
from views.main_window import MainWindow
from views.theme import APP_STYLESHEET


class Application:
    def __init__(self):
        self.stack = QStackedWidget()
        self.stack.setWindowTitle("Sistema de Controle de Estoque")
        self.stack.setMinimumSize(430, 540)
        self.stack.setStyleSheet(APP_STYLESHEET)
        self.login = LoginWindow()
        self.stack.addWidget(self.login)
        self.login.authenticated.connect(self.open_main)
        self.stack.show()

    def open_main(self, user: dict):
        self.main = MainWindow(user)
        self.main.logout_requested.connect(self.logout)
        self.stack.addWidget(self.main)
        self.stack.setMinimumSize(1080, 700)
        self.stack.setCurrentWidget(self.main)
        self.stack.resize(1440, 900)

    def logout(self):
        self.stack.setCurrentWidget(self.login)
        self.stack.setMinimumSize(430, 540)
        self.stack.resize(480, 600)
        self.main.deleteLater()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Controle de Estoque")
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)
    controller = Application()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
