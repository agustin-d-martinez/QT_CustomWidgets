from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys

import os, sys

from CustomWidgets.TitleBar import TitleBar
# Important:
# You need to run the following command to generate the ui_form.py file:
#     pyside6-rcc .\Icons\resources.qrc -o .\Icons\resources.py
# pyside6-designer
# from Icons import resources
class Application(QMainWindow):
    def __init__(self, parent= None ):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.titlebar = TitleBar(self)
        self.titlebar.setFixedHeight(50)
        self.button1 = QPushButton("Uno", self)
        self.button2 = QPushButton("Dos", self)
        self.button3 = QPushButton("Tres", self)

        layout  = QVBoxLayout()
        layout.addWidget(self.titlebar, alignment= Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.setContentsMargins(0,0,0,0)

        central = QWidget(self)
        central.setLayout(layout)
        
        self.setCentralWidget(central)
        self.grip = QSizeGrip(self)
        self.grip.resize(10, 10)

    def resizeEvent(self, event):
        self.grip.move(
            self.width() - self.grip.width(),
            self.height() - self.grip.height(),
        )
        return super().resizeEvent(event)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
