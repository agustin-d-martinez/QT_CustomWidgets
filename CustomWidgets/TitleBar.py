from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QMenu, QApplication, QStyle
from PySide6.QtGui import QIcon, QAction, QKeySequence, QMouseEvent
from PySide6.QtCore import Qt, QCoreApplication, QRect, QPoint, QMetaObject

from .QTDragHelper import QTDragHelper
from .SnapOverlay import SnapOverlay, SnapTarget

# TODO cerrar todo al agitar ???
# TODO it could be separated in mixin classes (context menu class, dragging class, snapping class)

class TitleBar(QWidget):
    SNAP_THRESHOLD = 5

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

        # Dragging
        self._normal_geometry = QRect()
        self.drag_helper = QTDragHelper()
        self._restore_ratio: float = 0.0
        self._drag_start_pos: QPoint | None = None

        # Context Menu
        self._context_menu = QMenu(self)
        style = QApplication.style()

        context_menu_restore = QAction(style.standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton), "Restaurar", self)
        context_menu_restore.triggered.connect(lambda: self.maximize_window(False))		
        context_menu_restore.setDisabled(True)

        context_menu_minimize = QAction(style.standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton), "Minimizar", self)
        context_menu_minimize.triggered.connect(self.minimize_window)	

        context_menu_maximize = QAction(style.standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton), "Maximizar", self)
        context_menu_maximize.triggered.connect(lambda: self.maximize_window(True))		

        context_menu_close = QAction(style.standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton), "Cerrar", self)
        context_menu_close.setShortcut(QKeySequence("ALT+F4"))
        context_menu_close.triggered.connect(self.close_window)
        
        self._context_menu.addAction(context_menu_restore)
        self._context_menu.addAction(context_menu_minimize)
        self._context_menu.addAction(context_menu_maximize)
        self._context_menu.addSeparator()
        self._context_menu.addAction(context_menu_close)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.exec_context_menu)

        # Visual Overlay
        self._overlay = SnapOverlay(self.window().screen())
        self._snap_target: SnapTarget = SnapTarget.NONE
 
        # Connects
        self.maximizeButton.clicked.connect(self.maximize_window)
        self.exitButton.clicked.connect(self.close_window)
        self.minimizeButton.clicked.connect(self.minimize_window)

        QMetaObject.connectSlotsByName(self)

# =====================================================
# QT Events
# =====================================================
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._drag_start_pos = event.globalPosition().toPoint()

        if self.window().isMaximized():
            self._restore_ratio = event.position().x() / self.width()

        self.drag_helper.pressed(self._drag_start_pos)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.globalPosition().toPoint()
        # Return if not draggin
        if not self.drag_helper.move(pos):  
            return

        # Maximized window
        if self.window().isMaximized():
            self.maximize_window(False)
            w = self._normal_geometry.width()
            h = self._normal_geometry.height()

            screen = self._screen_geometry_at(pos)
            new_x = int(pos.x() - w * self._restore_ratio)
            new_y = screen.top() + 10
            new_x = max(screen.left(), min(new_x, screen.right() - w))
            self.window().setGeometry(new_x, new_y, w, h)

            self.drag_helper.setLastPos(pos)
            return

        # Overlay
        self._update_overlay(pos)

        # drag normal
        dist = self.drag_helper.delta(pos)
        self.drag_helper.setLastPos(pos)
        self.window().move(self.window().pos() + dist)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        screen = self._screen_geometry_at(event.globalPosition().toPoint())
        self._overlay.hideOverlay()

        if self._snap_target == SnapTarget.MAXIMIZE:
            self.maximize_window(True)

        elif self._snap_target == SnapTarget.LEFT:
            self.window().setGeometry(
                screen.left(), screen.top(),
                screen.width() // 2, screen.height()
            )

        elif self._snap_target == SnapTarget.RIGHT:
            self.window().setGeometry(
                screen.center().x(), screen.top(),
                screen.width() // 2, screen.height()
            )

        self._snap_target = SnapTarget.NONE

        self.drag_helper.released()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.maximize_window(not self.window().isMaximized())

# =====================================================
# Functions
# =====================================================
    def maximize_window(self, check: bool = True) -> None:
        if check:
            if not self.window().isMaximized():
                self._normal_geometry = self.window().geometry()
            self.window().showMaximized()
            self.maximizeButton.setChecked(True)
            self._context_menu.actions()[0].setEnabled(True)
            self._context_menu.actions()[2].setDisabled(True)
        else:
            self.window().showNormal()
            self.maximizeButton.setChecked(False)
            self._context_menu.actions()[0].setDisabled(True)
            self._context_menu.actions()[2].setEnabled(True)

    def close_window(self) -> None:
        self._overlay.hideOverlay()
        self.window().close()
    
    def minimize_window(self) -> None:
        self.window().showMinimized()
    
    def exec_context_menu(self, pos: QPoint) -> None:
        self._context_menu.exec(self.mapToGlobal(pos))

# =====================================================
# Helpers
# =====================================================
    def _screen_geometry_at(self, pos: QPoint) -> QRect:
        screen = QApplication.screenAt(pos)
        if screen:
            return screen.availableGeometry()
        return self.window().screen().availableGeometry()

    def _update_overlay(self, pos: QPoint) -> None:
        if self.window().isMaximized():
            return

        screen = self._screen_geometry_at(pos)
        if pos.y() <= screen.top() + self.SNAP_THRESHOLD:
            self._snap_target = SnapTarget.MAXIMIZE
            self._overlay.showRect(screen)
        elif pos.x() <= screen.left() + self.SNAP_THRESHOLD:
            self._snap_target = SnapTarget.LEFT
            self._overlay.showRect(
                QRect(screen.left(), screen.top(),
                    screen.width() // 2, screen.height())
            )
        elif pos.x() >= screen.right() - self.SNAP_THRESHOLD:
            self._snap_target = SnapTarget.RIGHT
            self._overlay.showRect(
                QRect(screen.center().x(), screen.top(),
                    screen.width() // 2, screen.height())
            )
        else:
            self._snap_target = SnapTarget.NONE
            self._overlay.hideOverlay()
