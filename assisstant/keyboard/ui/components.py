from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush

class FlashingBox(QOpenGLWidget):

  def __init__(self, parent, freq, color):
    super(FlashingBox, self).__init__(parent)
    self.freq = freq
    self.brushes = [QBrush(Qt.black), QBrush(color)]
    self.index = 0
    self.enabled = False

  def timerEvent(self, event):
    if self.enabled:
        self.index = (self.index + 1) % 2
    else:
        self.index = 0
    self.update()

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.fillRect(event.rect(), self.brushes[self.index])
  
  def suspendFlashing(self):
    self.killTimer(self._timer)
    self.enabled=False
    self.index = 0
    self.update()
  
  def startFlashing(self):
    self.index = 0
    self.enabled = True
    delay = int(1000/(2 * self.freq))  #in mSec
    self._timer = self.startTimer(delay, Qt.PreciseTimer)


 
