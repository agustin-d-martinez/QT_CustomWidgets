from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from .QTDragHelper import QTDragHelper

# TODO añadir maximize al llegar arriba de todo.
# TODO cerrar todo al agitar ???
# TODO desminimizar al drag cuando esta en pantalla completa
# TODO añadir context menu

class TitleBar(QWidget):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setObjectName("TitleBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # size Policy
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # Size
        height = self.height()
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)

        # Layout
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.setObjectName(u"horizontalLayout")

        # Label
        app_name = QCoreApplication.applicationName()
        if not app_name:
            app_name = "App Name"
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText(app_name)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        # Spacer
        self.horizontalSpacer = QSpacerItem(369, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Minimize Button
        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setObjectName(u"exitButton")
        self.minimizeButton.setText("")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.minimizeButton.setIcon(icon)

        # Maximize Button
        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setObjectName(u"maximizeButton")
        self.maximizeButton.setText("")
        self.maximizeButton.setCheckable(True)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop))
        self.maximizeButton.setIcon(icon1)

        # Exit Button
        self.exitButton = QPushButton(self)
        self.exitButton.setObjectName(u"minimizeButton")
        self.exitButton.setText("")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowClose))
        self.exitButton.setIcon(icon2)

        # Connection to Layout
        horizontalLayout.addWidget(self.label)
        horizontalLayout.addItem(self.horizontalSpacer)
        horizontalLayout.addWidget(self.minimizeButton)
        horizontalLayout.addWidget(self.maximizeButton)
        horizontalLayout.addWidget(self.exitButton)
        horizontalLayout.setContentsMargins(0,0,0,0)

        # Drag Helper
        self.drag_helper = QTDragHelper()
        QMetaObject.connectSlotsByName(self)

        # Connects
        self.maximizeButton.clicked.connect(self.maximizeWindow)
        self.exitButton.clicked.connect(self.closeWindow)
        self.minimizeButton.clicked.connect(self.minimizeWindow)

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.globalPosition().toPoint()
        self.drag_helper.pressed(pos)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.globalPosition().toPoint()
        if not self.drag_helper.move(pos):  # Not draggin
            return
        
        # Is draggin
        dist = self.drag_helper.delta(pos)
        self.drag_helper.setLastPos(pos)
        self.window().move(self.window().pos() + dist)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_helper.released()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.maximizeWindow(True)

    def maximizeWindow(self, check: bool = True):
        if check:
            self.window().showMaximized()
            self.maximizeButton.setChecked(True)
        else:
            self.window().showNormal()
            self.maximizeButton.setChecked(False)

    def closeWindow(self):
        self.window().close()
    
    def minimizeWindow(self):
        self.window().showMinimized()