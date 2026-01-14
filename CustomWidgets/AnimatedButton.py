from PySide6.QtWidgets import *
from PySide6.QtCore import *

class AnimatedButton(QPushButton):
	def __init__(self, *args , **kwargs):
		QPushButton.__init__(self,*args,**kwargs)

		self.anim = QPropertyAnimation(self,b'geometry')
		self.anim.setDuration(500)
		self.anim.setEasingCurve(QEasingCurve.Type.OutExpo)
		
	def enterEvent(self, event):
		if self.anim.state() == self.anim.State.Stopped : 
			self.anim.setDirection(self.anim.Direction.Forward)
			rect = self.geometry()
			self.anim.setStartValue(rect)
			rect += QMargins(5,5,5,5)
			self.anim.setEndValue(rect)
			self.anim.start()
		return super().enterEvent(event)
	def leaveEvent(self, event):
		self.anim.setDirection(self.anim.Direction.Backward)
		if self.anim.state() == self.anim.State.Stopped : self.anim.start()
		return super().leaveEvent(event)

