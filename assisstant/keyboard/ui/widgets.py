from math import ceil
from PyQt5.QtCore import QRect, Qt, QTimer, pyqtProperty, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, pyqtSignal
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
  ui_pause = pyqtSignal(bool)
  ui_freeze = pyqtSignal(bool)
  send_query_signal = pyqtSignal(str)
  autocomplete_signal = pyqtSignal(str)

  def __init__(self):
    super(KeyboardWindow, self).__init__()
    self.initial_font = 17
    self.setupUi(self)
    self.target = None
    self.boxes = [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
    # for testing
    self.queries = [
        'What is the weather?',
        'in cairo',
        'weather in london,gb?'
    ]
    for index, box in enumerate(self.boxes):
      box.setFreq(config.FREQ[index])
      box.setColor(config.COLOR[index])

    # TODO: Create label for the undo box

    self.labels = [list()]
    self.row, self.col, self.interval = 0, 0, 8

    for i in range(self.interval):
      self.labels.append(list())
      for j in range(self.interval):
        # TODO: Use proper font size
        label = CustomLabel(self, self.initial_font)
        label.setText(config.CHARS[i][j])
        label.setStyleSheet("QLabel { color : rgba(255, 255, 255, 0.5); }")
        label.setAttribute(Qt.WA_TranslucentBackground)
        label.setAlignment(Qt.AlignCenter)
        label.show()
        self.labels[i].append(label)

  def resizeEvent(self, event):
    self.animate()

  def loadCharacters(self):
    for i in range(self.interval):
      for j in range(self.interval):
        self.labels[i][j].setText(config.CHARS[i][j])

  def resetCharacters(self):
    self.target = None
    selected = self.labels[self.row][self.col].text()
    # for testing
    # selected = "?"
    if selected == "?":
      # for testing
      self.ui_freeze.emit(True)
      if len(self.queries) == 0:
        self.send_query_signal.emit('2+2')
      else:
        self.send_query_signal.emit(self.queries.pop(0))
      # self.send_query_signal.emit(self.lblCmd.text())

    if len(selected) > 1:
      current_words = self.lblCmd.text().split(" ")
      print("current words: ", current_words)
      current_words[-1] = selected
      print(current_words)
      self.lblCmd.setText(" ".join(current_words) + " ")
    else:
      self.lblCmd.setText(self.lblCmd.text() + selected)
    self.row, self.col, self.interval = 0, 0, 8
    self.loadCharacters()
    self.updatePositions()
    QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, lambda: self.ui_pause.emit(False))

  def update_handler(self, result):
    self.interval //= 2
    if result == 0:
      pass
    elif result == 1:
      self.col += self.interval
    elif result == 2:
      self.row += self.interval
    elif result == 3:
      self.row += self.interval
      self.col += self.interval

    QTimer.singleShot(300, Qt.PreciseTimer, self.animate)

    if self.interval == 1:
      self.ui_pause.emit(True)
      self.target = result
      if len(self.labels[self.row][self.col].text()) > 1 or result == 0:
        QTimer.singleShot(1400, Qt.PreciseTimer, self.resetCharacters)
      else:
        self.ui_freeze.emit(True)
        self.autocomplete_signal.emit(self.lblCmd.text() + self.labels[self.row][self.col].text())

  def updatePositions(self):
    label_width = (self.gridLayout.geometry().width() - 2 * config.GRIDLAYOUT_MARGIN - config.GRIDLAYOUT_SPACING) // self.interval
    label_height = (self.gridLayout.geometry().height() - 2 * config.GRIDLAYOUT_MARGIN - config.GRIDLAYOUT_SPACING) // self.interval

    # TODO: Don't hide the labels that will remain
    for i in range(8):
      for j in range(8):
        self.labels[i][j].hide()

    animation_group = QParallelAnimationGroup(self)
    for pos in range(4):
      shiftx, shifty, idx_shiftx, idx_shifty = 0, 0, 0, 0
      if pos == 0:
        shiftx = config.GRIDLAYOUT_MARGIN
        shifty = config.GRIDLAYOUT_MARGIN
      elif pos == 1:
        shiftx = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        shifty = config.GRIDLAYOUT_MARGIN
        idx_shiftx = self.interval //2
      elif pos == 2:
        shiftx = config.GRIDLAYOUT_MARGIN
        shifty = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        idx_shifty = self.interval //2
      elif pos == 3:
        shiftx = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        shifty = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        idx_shiftx = self.interval //2
        idx_shifty = self.interval //2

      for i in range(idx_shifty,self.interval//2 + idx_shifty):
        for j in range(idx_shiftx,self.interval//2 + idx_shiftx):
          x = self.labels[i + self.row][j + self.col]
          x.show()
          x.set_font_size(self.initial_font)
          x.setGeometry(QRect(label_width * j + shiftx, label_height * i + shifty, label_width, label_height))

  def animate(self):
    label_width = (self.gridLayout.geometry().width() - 2 * config.GRIDLAYOUT_MARGIN - config.GRIDLAYOUT_SPACING) // self.interval
    label_height = (self.gridLayout.geometry().height() - 2 * config.GRIDLAYOUT_MARGIN - config.GRIDLAYOUT_SPACING) // self.interval

    # TODO: Don't hide the labels that will remain
    for i in range(8):
      for j in range(8):
        self.labels[i][j].hide()

    animation_group = QParallelAnimationGroup(self)
    for pos in range(4):
      if self.interval == 1 and pos != self.target:
        continue
      shiftx, shifty, idx_shiftx, idx_shifty = 0, 0, 0, 0
      if pos == 0:
        shiftx = config.GRIDLAYOUT_MARGIN
        shifty = config.GRIDLAYOUT_MARGIN
      elif pos == 1:
        shiftx = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        shifty = config.GRIDLAYOUT_MARGIN
        idx_shiftx = self.interval // 2
      elif pos == 2:
        shiftx = config.GRIDLAYOUT_MARGIN
        shifty = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        idx_shifty = self.interval // 2
      elif pos == 3:
        shiftx = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        shifty = config.GRIDLAYOUT_MARGIN + config.GRIDLAYOUT_SPACING
        idx_shiftx = self.interval // 2
        idx_shifty = self.interval // 2

      for i in range(idx_shifty, ceil(self.interval/2) + idx_shifty):
        for j in range(idx_shiftx, ceil(self.interval/2) + idx_shiftx):
          x = self.labels[i + self.row][j + self.col]
          x.show()
          if self.interval == 8:
            # TODO: Use proper font size
            x.set_font_size(self.initial_font)
            x.setGeometry(QRect(label_width * j + shiftx, label_height * i + shifty, label_width, label_height))
          else:
            easing_curve = QEasingCurve.InQuad
            animation = QPropertyAnimation(x, b'geometry', self)
            animation.setDuration(config.ANIMATION_DURATION)
            animation.setStartValue(x.geometry())
            if self.interval != 1:
              animation.setEndValue(QRect(label_width * j + shiftx , label_height * i +shifty , label_width, label_height))
            else:
              grdWidth = self.gridLayout.geometry().width()
              grdHeight = self.gridLayout.geometry().height()
              lblWidth = grdWidth
              lblHeight = grdHeight
              animation.setEndValue(QRect((grdWidth-lblWidth) / 2, (grdHeight-lblHeight)/2, lblWidth, lblHeight))
            animation.setEasingCurve(easing_curve)
            animation_group.addAnimation(animation)

            animation = QPropertyAnimation(x, b'font_size', self)
            animation.setDuration(config.ANIMATION_DURATION)
            animation.setStartValue(x.font_size)
            animation.setEndValue(min(label_width, label_height) / 2)
            animation.setEasingCurve(easing_curve)
            animation_group.addAnimation(animation)

      animation_group.start()

  def flash(self):
    for box in self.boxes:
      box.startFlashing()

  def unflash(self):
    for box in self.boxes:
      box.stopFlashing()

  def flash_handler(self, value):
    if self.interval == 1:
      return
    if value:
      print("Flash: on")
      self.flash()
    else:
      print("Flash: off")
      self.unflash()

  def unfreeze(self):
    self.ui_freeze.emit(False)

  def receive_query_response(self, action):
    if action:
      print(action.type)
      print(action.body)
      self.undo.setText(str(action.body))
    QTimer.singleShot(5000, Qt.PreciseTimer, self.unfreeze)

  def receive_predicted_words(self, words):
    self.unfreeze()
    if len(words) < 3:
      QTimer.singleShot(1400, Qt.PreciseTimer, self.resetCharacters)
    else:
      self.interval = 2
      selected_char = self.labels[self.row][self.col].text()
      self.row, self.col = 0, 0
      self.labels[self.row][self.col].setText(selected_char)
      self.updatePositions()
      idx = 0
      for i in range(self.interval):
        for j in range(self.interval):
          if idx > 0:
            self.labels[i+self.row][j+self.col].setText(words[idx - 1][0])
          idx += 1
      QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, lambda: self.ui_pause.emit(False))

    # self.interval = 