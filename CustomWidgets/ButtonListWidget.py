from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QListWidgetItem, QAbstractItemView, QSizePolicy, QVBoxLayout, QHBoxLayout, QStyle
from PySide6.QtGui import QResizeEvent, QIcon
from PySide6.QtCore import Qt, QMargins, QSize

from .DroppableList import DroppableList

class ButtonListWidget(QWidget):
    """
    Buttoned list widget. Adds 4 buttons to a QListWidget for adding, removing, moving up and moving down.
    """
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setObjectName("ButtonListWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Exponer el QListWidget como un atributo público
        self.listWidget = DroppableList()
        self.listWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

        # Layout para los botones (Vertical)
        buttons_container = QWidget(self)
        buttons_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding )
        button_layout = QVBoxLayout(buttons_container)
        button_layout.setSpacing(4)
        button_layout.setContentsMargins(QMargins(4,4,4,4))

        # Crear botones
        self._btn_add = QPushButton()
        self._btn_remove = QPushButton()
        self._btn_up = QPushButton()
        self._btn_down = QPushButton()
        self._btn_add.setObjectName("btnAdd")
        self._btn_remove.setObjectName("btnRemove")
        self._btn_up.setObjectName("btnUp")
        self._btn_down.setObjectName("btnDown")

        style = self.style()                # Default Button Style
        self._btn_add.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder))
        self._btn_remove.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        self._btn_up.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowUp))
        self._btn_down.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowDown))

        for btn in [self._btn_add, self._btn_remove, self._btn_up, self._btn_down]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        button_layout.addWidget(self._btn_add)
        button_layout.addWidget(self._btn_remove)
        button_layout.addWidget(self._btn_up)
        button_layout.addWidget(self._btn_down)

        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.listWidget, 10)
        main_layout.addWidget(buttons_container, 1)
        main_layout.setContentsMargins(QMargins(6,6,6,6))
        main_layout.setSpacing(6)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Conectar botones con funciones
        self._btn_add.clicked.connect(self.add_item)
        self._btn_remove.clicked.connect(self.remove_item)
        self._btn_up.clicked.connect(self.move_item_up)
        self._btn_down.clicked.connect(self.move_item_down)

        #Conect para habilitar botones
        self.listWidget.model().rowsInserted.connect(self.UpdateButtons)
        self.listWidget.model().rowsRemoved.connect(self.UpdateButtons)
        self.listWidget.itemSelectionChanged.connect(self.UpdateButtons)

        self.UpdateButtons()

    def UpdateButtons(self):
        item_count = self.listWidget.count()
        has_selection = bool(self.listWidget.selectedItems())
        row = self.listWidget.currentRow()

        self._btn_add.setEnabled(True)
        self._btn_remove.setEnabled(has_selection)
        self._btn_up.setEnabled(has_selection and row > 0)
        self._btn_down.setEnabled(has_selection and row < item_count - 1)

    def resizeEvent(self, event: QResizeEvent) -> None:
        available_height = self.height()
        btn_height = max(24, min(available_height // 4 - 6, 48))
        icon_size = int(btn_height * 0.7)

        for btn in [self._btn_add, self._btn_remove, self._btn_up, self._btn_down]:
            btn.setFixedHeight(btn_height)
            btn.setIconSize(QSize(icon_size, icon_size))

        super().resizeEvent(event)

    def add_item(self):
        """Agrega un nuevo elemento a la lista."""
        item = QListWidgetItem("")  
        self.listWidget.addItem(item)  
        self.listWidget.setCurrentItem(item)  
        # self.listWidget.editItem(item)

        ## Crear un editor manualmente
        editor = QLineEdit(self.listWidget)  
        self.listWidget.setItemWidget(item, editor)  # Asignar el editor al item
        editor.setFocus()  
        editor.selectAll()  

        # Guardar el texto en el item cuando el usuario termine de editar
        editor.editingFinished.connect(lambda: self.finalizar_edicion(item, editor))

    def finalizar_edicion(self, item: QListWidgetItem, editor: QLineEdit):
        self.listWidget.setItemWidget(item, None)  # Remover el editor
        text = editor.text()
        if not text :
            self.remove_item()
        else:
            item.setText(editor.text())  
    
    def remove_item(self):
        """Elimina el elemento seleccionado."""
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

    def move_item_up(self):
        """Mueve el elemento seleccionado hacia arriba."""
        row = self.listWidget.currentRow()
        if row > 0:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, item)
            self.listWidget.setCurrentItem(item)

    def move_item_down(self):
        """Mueve el elemento seleccionado hacia abajo."""
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, item)
            self.listWidget.setCurrentItem(item)
    
    def setIcons(self, add: QIcon | None = None, remove: QIcon | None = None, up: QIcon | None = None, down: QIcon | None = None) -> None:
        if add is not None:
            self._btn_add.setIcon(add)
        if remove is not None:
            self._btn_remove.setIcon(remove)
        if up is not None:
            self._btn_up.setIcon(up)
        if down is not None:
            self._btn_down.setIcon(down)
