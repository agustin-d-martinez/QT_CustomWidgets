from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


# Important:
# You need to run the following command to generate the ui_form.py file:
#     pyside6-rcc .\Icons\resources.qrc -o .\Icons\resources.py
# pyside6-designer
# from Icons import resources
# pyinstaller --onefile --windowed --name="MyLovePDF" --icon=resources/Icons/app_icon.ico  mainwindow.py

class FramelessWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set GRIP
        self.grip = QSizeGrip(self)
        self.grip.resize(10, 10)

        # Set Drag
        self.dragStartPos = None
        self.dragPos = None
        self.normalGeometry = self.geometry()
        self.drag_state = self.DRAG_NONE
        self.dragRatioX = None
        self.ignoreRelease = False
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.ui.exit_frame.mousePressEvent = self._titleBar_mousePressEvent
        self.ui.exit_frame.mouseMoveEvent = self._titleBar_mouseMoveEvent
        self.ui.exit_frame.mouseReleaseEvent = self._titleBar_mouseReleaseEvent
        self.ui.exit_frame.mouseDoubleClickEvent = self._titleBar_mouseDoubleClickEvent

        # -----------------------------------------------------------
        # Set Connect Functions
        # -----------------------------------------------------------
        # Exit menu
        self.ui.close_button.clicked.connect(self.close)
        self.ui.minimize_button.clicked.connect(self.showMinimized)
        self.ui.maximize_button.clicked.connect(self.update_window_size)

    # ----------------------------------------------
    # Maximize/Restore Functions
    # ----------------------------------------------
    # DEFINE DRAG STATES
    DRAG_NONE = 0
    DRAG_ARMING = 1  
    DRAGGING = 2
    def update_window_size(self, checked):
        if checked:
            self.normalGeometry = self.geometry()
            self.showMaximized()
            self.grip.hide()
        else:
            self.showNormal()
            self.grip.show()
    
    def _titleBar_mousePressEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        # Start values of drag and release logic
        self.drag_state = self.DRAG_ARMING
        self.dragStartPos = event.globalPosition().toPoint()
        if self.isMaximized():
            self.dragRatioX = event.position().x() / self.width()
        else:
            self.dragRatioX = None
        self.dragPos = self.dragStartPos - self.frameGeometry().topLeft()
        event.accept()
    
    def _titleBar_mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() != Qt.MouseButton.LeftButton:
            return
        
        # dragg logic         
        dist = (event.globalPosition().toPoint() - self.dragStartPos).manhattanLength()
        if self.drag_state == self.DRAG_NONE or dist < 10:
            return
        self.drag_state = self.DRAGGING

        # if maximized, restore and move
        if self.isMaximized():
            self.ui.maximize_button.setChecked(False)
            self.update_window_size(False)

            normal_widht = self.normalGeometry.width()
            mouse_x = event.globalPosition().toPoint().x()
            mouse_y = event.globalPosition().toPoint().y()

            x = int(mouse_x - self.dragRatioX * normal_widht)
            self.move(x, mouse_y)

            self.dragPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.dragRatioX = None
            event.accept()
            return
        self.move(event.globalPosition().toPoint() - self.dragPos)
        event.accept()

    def _titleBar_mouseReleaseEvent(self, event: QMouseEvent):
        # Ignore mouse Release. Used in double click maximize.
        if self.ignoreRelease:
            self.ignoreRelease = False
            self.drag_state = self.DRAG_NONE
            event.accept()
            return
        
        # If not dragging, do nothing
        if self.drag_state != self.DRAGGING:
            event.accept()
            return
        
        # if dragging, check "snap to maximize" 
        self.drag_state = self.DRAG_NONE
        if event.globalPosition().toPoint().y() <= 5:
            self.ui.maximize_button.setChecked(True)
            self.update_window_size(True)
        else:
            self.ui.maximize_button.setChecked(False)
            self.update_window_size(False)
        event.accept()

    def _titleBar_mouseDoubleClickEvent(self, event: QMouseEvent):
        # Double click maximize/restore logic
        self.ignoreRelease = True
        is_not_maximized = not self.isMaximized()
        self.ui.maximize_button.setChecked(is_not_maximized)
        self.update_window_size(is_not_maximized)
        event.accept()

    def resizeEvent(self, event):
        self.grip.move(
            self.width() - self.grip.width(),
            self.height() - self.grip.height(),
        )
        return super().resizeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    # app.setApplicationName("MyLovePDF")
    # app.setWindowIcon(QIcon(":/Icons/App_icon.ico"))

    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())