# coding: utf8
from PySide6 import QtWidgets, QtCore
from jnp3.gui import StyleComboBox


class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cmbx_styles = StyleComboBox(self)

    def sizeHint(self):
        return QtCore.QSize(300, 100)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    win = MainWindow()
    win.show()
    app.exec()
