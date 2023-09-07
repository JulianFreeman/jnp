# coding: utf8
from enum import IntEnum, unique
from PySide6 import QtWidgets


@unique
class ItemUserRole(IntEnum):
    StatusRole = 0x0101
    IdsRole = 0x0102
    UrlRole = 0x0103
    SizeRole = 0x0104


def accept_warning(widget: QtWidgets.QWidget, condition: bool,
                   caption: str = "Warning", text: str = "Are you sure to continue?") -> bool:
    if condition:
        b = QtWidgets.QMessageBox.question(widget, caption, text)
        if b == QtWidgets.QMessageBox.StandardButton.No:
            return True
    return False
