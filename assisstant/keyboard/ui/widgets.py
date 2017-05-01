from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import QRect, Qt, QTimer, QPropertyAnimation, pyqtProperty, QParallelAnimationGroup
from PyQt5.QtGui import QFont
from .keyboard_ui import Ui_KeyboardWindow
from keyboard import config
from math import sqrt


class CustomLabel(QLabel):
  def __init__(self, parent, size):
    super().__init__()
    self.setParent(parent)
    self._font_size = size
    self.setFont(QFont("MONO", size))

  @pyqtProperty(int)
  def font_size(self):
    return self._font_size

  @font_size.setter
  def font_size(self, size):
    self._font_size = size
    self.setFont(QFont("MONO", size))

  def set_font_size(self, size):
    self._font_size = size
    self.setFont(QFont("MONO", size))

class KeyboardWindow(QMainWindow, Ui_KeyboardWindow):
  def __init__(self):
    super(KeyboardWindow, self).__init__()
    self.setupUi(self)
    self.boxes = [self.top_left, self.top_right, self.bottom_left, self.bottom_right, self.undo]
    self.gridLayout.layout()
    self.labels = []
    self.begin = 0
    self.end = 63
    for i in range(64):
      x = CustomLabel(self, 55)
      x.setText(chr(i + 65))
      x.setStyleSheet("QLabel { color : white; }")
      x.setAttribute(Qt.WA_TranslucentBackground)
      x.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
      x.show()
      self.labels.append(x)

    for index, box in enumerate(self.boxes):
      box.setFreq(config.FREQ[index])
      box.setColor(config.COLOR[index])

  def update_handler(self, result):
    newInterval = (self.end-self.begin+1)//4
    if newInterval == 1:
      self.lblCmd.setText(self.lblCmd.text() + self.labels[self.begin + result].text())
      self.begin = 0
      self.end = 63
    else:
      self.begin = self.begin + result*newInterval
      self.end = self.begin + newInterval - 1

  def animate(self):
    interval = self.end-self.begin+1
    quarter = interval//4
    row = int(sqrt(quarter))
    col = int(sqrt(quarter))

    layout_width = self.gridLayout.geometry().width()
    layout_height = self.gridLayout.geometry().height()
    label_width = layout_width//(row*2)
    label_height = layout_height//(col*2)

    duration = 200

    for label in self.labels:
      label.hide()

    for index in range(self.begin, self.end + 1):
      self.labels[index].show()

    animationGroup = QParallelAnimationGroup(self)
    for boxi in range(2):
      for boxj in range(2):
        for i in range(row):
          for j in range(col):
            x = self.labels[self.begin + (2*boxi + boxj) * quarter + i*row + j]
            if interval == 64:
              x.set_font_size(55)
              x.setGeometry(QRect(label_width * j + boxj*layout_width/2,
                                  label_height * i + boxi*layout_height/2,
                                  label_width, label_height))
            else:
              animation = QPropertyAnimation(x, b'geometry', self)
              animation.setDuration(duration)
              animation.setStartValue(x.geometry())
              animation.setEndValue(QRect(label_width * j + boxj*layout_width/2,
                                          label_height * i + boxi*layout_height/2,
                                          label_width, label_height))
              animationGroup.addAnimation(animation)

              animation = QPropertyAnimation(x, b'font_size', self)
              animation.setDuration(duration)
              animation.setStartValue(x.font_size)
              animation.setEndValue(min(label_width, label_height)/1.5)
              animationGroup.addAnimation(animation)

    animationGroup.start()

  def start(self):
    # TODO: Remove this delay, it waits for the grid initialization
    QTimer.singleShot(200, Qt.PreciseTimer, self.animate)

    # Brief pause before flashing, it makes the first second of recording corrupted
    QTimer.singleShot(1000, Qt.PreciseTimer, self.flash)

  def flash(self):
    for box in self.boxes:
      box.startFlashing()

  def unflash(self):
    for box in self.boxes:
      box.stopFlashing()

  def flash_handler(self, value):
    if value:
      print("Flash: on")
      self.start()
    else:
      print("Flash: off")
      self.unflash()
