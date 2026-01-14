from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import * 

class DroppableImageLabel(QLabel):
	"""
	QLabel for images with drag and drop support. 
	Includes a context menu for cut, copy, paste, delete and add photo.
	"""
	def __init__(self, parent, editable=True, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.setScaledContents(True)
		self.setAcceptDrops(True)				## Para poder tirarle fotos
		self.default_pixmap = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon).pixmap(64,64)
		self.setPixmap(self.default_pixmap)	## Chequear 	
		self._context_menu = QMenu(self)

		action_cut = QAction(QIcon.fromTheme("edit-cut"),"Cortar",self)
		action_cut.setShortcut(QKeySequence("CTRL+X"))
		action_cut.triggered.connect(self.cut)		

		action_copy = QAction(QIcon.fromTheme("edit-copy"),"Copiar",self)
		action_copy.setShortcut(QKeySequence("CTRL+C"))		
		action_copy.triggered.connect(self.copy)	

		action_paste = QAction(QIcon.fromTheme("edit-paste"),"Pegar",self)
		action_paste.setShortcut(QKeySequence("CTRL+V"))
		action_paste.triggered.connect(self.paste)		

		action_delete = QAction(QIcon.fromTheme("edit-delete"),"Borrar",self)
		action_delete.setShortcut(Qt.Key.Key_Delete)
		action_delete.triggered.connect(self.delete)
		
		action_add = QAction(QIcon.fromTheme("edit-add"),"Añadir",self)
		action_add.setShortcut(QKeySequence("CTRL+A"))
		action_add.triggered.connect(self.addPhoto)

		self._context_menu.addAction(action_cut)
		self._context_menu.addAction(action_copy)
		self._context_menu.addAction(action_paste)
		self._context_menu.addAction(action_delete)
		self._context_menu.addSeparator()
		self._context_menu.addAction(action_add)

		if editable:
			self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
			self.customContextMenuRequested.connect(self.execContextMenu)

	def execContextMenu(self, pos: QPoint) -> None:
		self._context_menu.exec(self.mapToGlobal(pos))
	def cut (self):
		self.copy()
		self.delete()
	def copy (self):
		clipboard = QApplication.clipboard()
		pixmap = self.pixmap()
		if pixmap :
			clipboard.setPixmap(pixmap)
	def paste (self):
		pixmap = QApplication.clipboard().pixmap()
		if not pixmap.isNull():
			self.setPixmap(pixmap)
	def delete(self):
		self.clear()
		self.setPixmap(self.default_pixmap)
		self.update()

	def addPhoto(self):
		archivo, _ = QFileDialog.getOpenFileName(self,"Seleccionar archivo","","Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)")
		if archivo:
			self.setPixmap(QPixmap(archivo))

	def dragEnterEvent(self, event: QDragEnterEvent):
		if event.mimeData().hasImage() or event.mimeData().hasUrls():
			event.accept()
		else : 
			event.ignore()

	def dragMoveEvent(self, event: QDragMoveEvent):
		if event.mimeData().hasImage() or event.mimeData().hasUrls():
			event.setDropAction(Qt.DropAction.CopyAction)
			event.accept()
		else : 
			event.ignore()

	def dropEvent(self, event: QDropEvent):
		if event.mimeData().hasImage() : 
			event.setDropAction(Qt.DropAction.CopyAction)
			event.accept()
			image = event.mimeData().imageData()
			if isinstance(image, QImage):
				pixmap = QPixmap.fromImage(image)
			else:
				pixmap = image
		elif event.mimeData().hasUrls():
			url = event.mimeData().urls()[0]
			if url.isLocalFile():
				event.setDropAction(Qt.DropAction.CopyAction)
				event.accept()
				pixmap = QPixmap.fromImage(QImage(url.toLocalFile()))
			else:
				event.ignore()
				return
		else :
			event.ignore()
			return
		
		self.setPixmap(pixmap)
		self.update()

	def setDefaultPixmap(self, pixmap: QPixmap | None) -> None:
		if pixmap is None or pixmap.isNull():
			self.default_pixmap = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon).pixmap(64,64)
		else:
			self.default_pixmap = pixmap


