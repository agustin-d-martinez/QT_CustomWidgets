from PySide6.QtWidgets import QListWidget, QMenu, QAbstractItemView, QFileDialog
from PySide6.QtCore import QPoint, QFileInfo
from PySide6.QtGui import Qt, QKeyEvent, QDragEnterEvent, QDragMoveEvent, QDropEvent

class DroppableList(QListWidget):
    """
    QListWidget with drag and drop support for files. 
    Includes a context menu for adding, removing, and moving items. 
    Includes key press event handling for deleting items with the Delete key.
    """
    def __init__(self, parent = None, file_type_filter: str = "*.*", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setObjectName("DroppableListWidget")
        self.setAcceptDrops(True)

        self.context_menu = QMenu("",self)
        self.context_menu.addAction("Agregar Archivo", self.addFile)
        self.context_menu.addAction("Borrar archivo", self.delFile)
        self.context_menu.addAction("Subir", self.UpFile)
        self.context_menu.addAction("Bajar", self.DownFile)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.execContextMenu)
        
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.file_type_filter = file_type_filter
        self.last_file_dir = ""

    def execContextMenu(self, pos: QPoint) -> None:
        # Disable if not selected
        has_selection = bool(self.selectedItems())
        item_count = self.count()
        has_selection = self.currentItem() is not None
        row = self.currentRow()

        self.context_menu.actions()[1].setEnabled(has_selection)  
        self.context_menu.actions()[2].setEnabled(has_selection and row > 0)  
        self.context_menu.actions()[3].setEnabled(has_selection and row < item_count - 1)  

        self.context_menu.exec(self.mapToGlobal(pos))

    def addFile(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivo", self.last_file_dir, self.file_type_filter)
        existing_files = {self.item(i).text() for i in range(self.count())}

        for file in files:
            if file not in existing_files:
                self.addItem(file)
        if files:
            self.last_file_dir = QFileInfo(files[0]).absolutePath()

    def UpFile(self) -> None:
        rows = sorted([self.row(item) for item in self.selectedItems()])
        if not rows or rows[0] == 0:
            return  # No se puede subir si el primer ítem seleccionado está en la posición 0
        for row in rows:
            item = self.takeItem(row)
            self.insertItem(row - 1, item)
            item.setSelected(True)

    def DownFile(self) -> None:
        rows = sorted([self.row(item) for item in self.selectedItems()], reverse=True)
        if not rows or rows[0] == self.count() - 1:
            return  # No se puede bajar si el último ítem seleccionado ya está en la última posición
        for row in rows:
            item = self.takeItem(row)
            self.insertItem(row + 1, item)
            item.setSelected(True)

    def delFile(self) -> None:
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key in [Qt.Key.Key_Delete, Qt.Key.Key_Backspace]:
            self.delFile()
        super().keyPressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls:
            event.accept()
        else : 
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else : 
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls : 
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls() :
                if url.isLocalFile() : 
                    links.append(url.toLocalFile())
                    ## links.append(url.toString()) ##Para links de internet
            self.addItems(links)
        else : 
            event.ignore()