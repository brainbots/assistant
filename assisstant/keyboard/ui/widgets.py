from PyQt5.QtCore import QRect, Qt, QTimer, pyqtProperty, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel

from keyboard import config
from .keyboard_ui import Ui_KeyboardWindow


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
    self.gridLayout.layout()

    self.boxes = [self.top_left, self.top_right, self.bottom_left, self.bottom_right, self.undo]
    for index, box in enumerate(self.boxes):
      box.setFreq(config.FREQ[index])
      box.setColor(config.COLOR[index])

    self.labels = [list()]
    self.row, self.col, self.interval = 0, 0, 8

    for i in range(self.interval):
      self.labels.append(list())
      for j in range(self.interval):
        # TODO: Use proper font size
        label = CustomLabel(self, 55)
        label.setText(config.CHARS[i][j])
        label.setStyleSheet("QLabel { color : white; }")
        label.setAttribute(Qt.WA_TranslucentBackground)
        label.setAlignment(Qt.AlignCenter)
        label.show()
        self.labels[i].append(label)

  def update_handler(self, result):
    self.interval //= 2
    if self.interval == 1:
      if result == 0:
        self.lblCmd.setText(self.lblCmd.text() + self.labels[self.row][self.col].text())
      elif result == 1:
        self.lblCmd.setText(self.lblCmd.text() + self.labels[self.row][self.col + 1].text())
      elif result == 2:
        self.lblCmd.setText(self.lblCmd.text() + self.labels[self.row + 1][self.col].text())
      elif result == 3:
        self.lblCmd.setText(self.lblCmd.text() + self.labels[self.row + 1][self.col + 1].text())

      self.row, self.col, self.interval = 0, 0, 8

    else:
      if result == 0:
        pass
      elif result == 1:
        self.col += self.interval
      elif result == 2:
        self.row += self.interval
      elif result == 3:
        self.row += self.interval
        self.col += self.interval

  def animate(self):
    label_width = self.gridLayout.geometry().width() // self.interval
    label_height = self.gridLayout.geometry().height() // self.interval

    # TODO: Don't hide the labels that will remain
    for i in range(8):
      for j in range(8):
        self.labels[i][j].hide()

    animation_group = QParallelAnimationGroup(self)
    for i in range(self.interval):
      for j in range(self.interval):
        x = self.labels[i + self.row][j + self.col]
        x.show()
        if self.interval == 8:
          # TODO: Use proper font size
          x.set_font_size(55)
          x.setGeometry(QRect(label_width * j, label_height * i, label_width, label_height))
        else:
          easing_curve = QEasingCurve.InQuad

          animation = QPropertyAnimation(x, b'geometry', self)
          animation.setDuration(config.ANIMATION_DURATION)
          animation.setStartValue(x.geometry())
          animation.setEndValue(QRect(label_width * j, label_height * i, label_width, label_height))
          animation.setEasingCurve(easing_curve)
          animation_group.addAnimation(animation)

          animation = QPropertyAnimation(x, b'font_size', self)
          animation.setDuration(config.ANIMATION_DURATION)
          animation.setStartValue(x.font_size)
          animation.setEndValue(min(label_width, label_height) / 1.5)
          animation.setEasingCurve(easing_curve)
          animation_group.addAnimation(animation)

    animation_group.start()

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
