# coding: utf8
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QWidget


class PushButtonWithId(QPushButton):

    clicked_with_id = Signal(str)

    def __init__(self, ids: str, parent: QWidget = None, title: str = ""):
        super().__init__(title, parent)
        self.ids = ids
        self.clicked.connect(self.on_self_clicked)

    def on_self_clicked(self):
        self.clicked_with_id.emit(self.ids)
