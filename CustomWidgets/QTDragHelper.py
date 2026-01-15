from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QPoint

class QTDragHelper():
    # It could be a class(enum). Its just more complex and pointless for the aplication
    DRAG_NONE = 0
    DRAG_ARMING = 1  
    DRAGGING = 2
    
    def __init__(self, threashold_dist: int | None = None):
        self._state = self.DRAG_NONE
        self._start_pos = QPoint()
        self._last_pos = QPoint()
        self.threashold_dist = (
            threashold_dist 
            if threashold_dist 
            else QApplication.startDragDistance()
        )

    def pressed(self, pos: QPoint) -> None:
        self._state = self.DRAG_ARMING
        self._start_pos = pos
        self._last_pos = pos

    def move(self, pos: QPoint) -> bool:
        if self._state == self.DRAG_NONE:
            return False
        
        dist = (pos - self._start_pos).manhattanLength()
        if dist >= self.threashold_dist:
            self._state = self.DRAGGING
            return True       
        return False

    def setLastPos(self, pos: QPoint) -> None:
        self._last_pos = pos

    def delta(self, pos: QPoint) -> QPoint:
        return pos - self._last_pos

    def isDragging(self) -> bool:
        return self._state == self.DRAGGING

    def released(self) -> bool:
        was_dragging = self._state == self.DRAGGING
        self._state = self.DRAG_NONE

        return was_dragging