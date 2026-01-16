from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
import os

from CustomWidgets.TitleBar import TitleBar
from CustomWidgets.FramelessWindow import FramelessWindow
# Important:
# You need to run the following command to generate the ui_form.py file:
#     pyside6-rcc .\Icons\resources.qrc -o .\Icons\resources.py
# pyside6-designer
# from Icons import resources

class Application(FramelessWindow):
    def __init__(self, parent= None ):
        super().__init__(parent)

        self.titlebar = TitleBar(self)
        self.titlebar.setFixedHeight(50)
        self.titlebar.setStyleSheet(
            """#TitleBar { color: white; }\n
            QWidget{ background-color: #000000;}\n
            QPushButton{ background-color: grey;}\n
            QLabel{color: white;}\n 
            QAction{color: white;}"""
        )
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())
