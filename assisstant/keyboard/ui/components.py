from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QFont, QPen, QColor

class FlashingBox(QOpenGLWidget):
  def __init__(self, parent, freq=1, color=Qt.black):
    super(FlashingBox, self).__init__(parent)
    self.freq = freq
    self.brushes = [QBrush(Qt.black), QBrush(color)]
    self.index = 1
    self.enabled = False

  def setFreq(self, freq):
    self.freq = freq

  def setColor(self, color):
    self.brushes[1] = QBrush(color)

  def timerEvent(self, event):
    if self.enabled:
      self.index = (self.index + 1) % 2
    else:
      self.index = 0
    self.update()

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.fillRect(event.rect(), self.brushes[self.index])

  def startFlashing(self):
    self.index = 0
    self.enabled = True
    delay = int(1000/(2 * self.freq))  #in mSec
    self._timer = self.startTimer(delay, Qt.PreciseTimer)

  def stopFlashing(self):
    self.killTimer(self._timer)
    self.enabled=False
    self.index = 0
    self.update()
