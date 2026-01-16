from PySide6.QtWidgets import QMainWindow, QApplication, QWidget
from PySide6.QtCore import Qt, QPoint, QRect, QEvent

class FramelessWindow(QMainWindow):
    BORDER = 6

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Set Drag
        self.setWindowFlag(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setMouseTracking(True)
        QApplication.instance().installEventFilter(self)


        self._resizing = False
        self._resize_region = Qt.Edge()
        self._press_pos_global = QPoint()
        self._start_geometry = QRect()

    def eventFilter(self, obj, event):
        if not isinstance(obj, QWidget):
            return False
        if obj is not self and not self.isAncestorOf(obj):
            return False

        if self._handle_resize_event(event):
            return True
        return super().eventFilter(obj, event)
    
    def _handle_resize_event(self, event):
        et = event.type()

        # Mouse move
        if et == QEvent.Type.MouseMove:
            if self.isMaximized():
                return False
            global_pos = event.globalPosition().toPoint()
            local_pos = self.mapFromGlobal(global_pos)

            if self._resizing:
                self._resize_window(global_pos)
                return True

            region = self._edges_at(local_pos)
            cursor = self._cursor_for_edges(region)
            if self.cursor().shape() != cursor:
                self.setCursor(cursor)

        # Mouse press
        elif et == QEvent.Type.MouseButtonPress:
            if event.button() != Qt.MouseButton.LeftButton:
                return False
            if self.isMaximized():
                return False
            local_pos = self.mapFromGlobal(event.globalPosition().toPoint())
            region = self._edges_at(local_pos)

            if region != Qt.Edge():
                self._resizing = True
                self._resize_region = region
                self._press_pos_global = event.globalPosition().toPoint()
                self._start_geometry = self.geometry()
                return True

        # Mouse release
        elif et == QEvent.Type.MouseButtonRelease:
            if self._resizing:
                self._resizing = False
                self._resize_region = Qt.Edge()
                return True

        return False

    def _edges_at(self, pos: QPoint) -> Qt.Edge:
        rect = self.rect()
        x, y = pos.x(), pos.y()
        b = self.BORDER

        region = Qt.Edge()

        if x <= b:
            region = Qt.Edge.LeftEdge
        elif x >= rect.width() - b:
            region = Qt.Edge.RightEdge

        if y <= b:
            region |= Qt.Edge.TopEdge
        elif y >= rect.height() - b:
            region |= Qt.Edge.BottomEdge

        return region

    def _cursor_for_edges(self, edges: Qt.Edges) -> Qt.CursorShape:
        if edges == (Qt.Edge.LeftEdge | Qt.Edge.TopEdge) or edges == (Qt.Edge.RightEdge | Qt.Edge.BottomEdge):
            return Qt.CursorShape.SizeFDiagCursor

        if edges == (Qt.Edge.RightEdge | Qt.Edge.TopEdge) or edges == (Qt.Edge.LeftEdge | Qt.Edge.BottomEdge):
            return Qt.CursorShape.SizeBDiagCursor

        if edges & (Qt.Edge.LeftEdge | Qt.Edge.RightEdge):
            return Qt.CursorShape.SizeHorCursor

        if edges & (Qt.Edge.TopEdge | Qt.Edge.BottomEdge):
            return Qt.CursorShape.SizeVerCursor

        return Qt.CursorShape.ArrowCursor

    def _resize_window(self, global_pos: QPoint) -> None:
        delta = global_pos - self._press_pos_global
        geom = QRect(self._start_geometry)

        min_size = self.minimumSizeHint()
        min_w = min_size.width()
        min_h = min_size.height()

        if Qt.Edge.LeftEdge in self._resize_region:
            right = geom.right()
            new_left = self._start_geometry.left() + delta.x()
            max_left = right - min_w + 1
            geom.setLeft(min(new_left, max_left))


        if Qt.Edge.RightEdge in self._resize_region:
            new_w = geom.width() + delta.x()
            geom.setWidth(max(new_w, min_w))

        if Qt.Edge.TopEdge in self._resize_region:
            bottom = geom.bottom()
            new_top = self._start_geometry.top() + delta.y()
            max_top = bottom - min_h + 1
            geom.setTop(min(new_top, max_top))

        if Qt.Edge.BottomEdge in self._resize_region:
            new_h = geom.height() + delta.y()
            geom.setHeight(max(new_h, min_h))

        self.setGeometry(geom)
