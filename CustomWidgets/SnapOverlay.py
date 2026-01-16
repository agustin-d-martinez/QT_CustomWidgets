from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from enum import Enum

class SnapTarget(Enum):
    NONE = 0
    MAXIMIZE = 1
    LEFT = 2
    RIGHT = 3


class SnapOverlay(QWidget):
    def __init__(self, screen: QScreen):
        super().__init__(None)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.BypassWindowManagerHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._rect = QRect()
        self.setGeometry(screen.geometry())
        self.hide()

    def showRect(self, rect: QRect):
        self._rect = rect
        self.show()
        self.raise_()
        self.update()

    def hideOverlay(self):
        self.hide()

    def paintEvent(self, event):
        if self._rect.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(0, 120, 215, 80)  # azul estilo Windows
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRoundedRect(self._rect, 6, 6)
