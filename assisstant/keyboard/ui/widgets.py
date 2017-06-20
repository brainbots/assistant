from math import ceil
from PyQt5.QtCore import QRect, Qt, QTimer, pyqtProperty, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, pyqtSignal

from PyQt5.QtGui import QFont, QWindow, QTextCursor
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout

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
    self.autocomplete = False
    self.boxes = [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
    # for testing
    self.queries = [
        'What is the weather?',
        'in cairo',
        'weather in london,gb?'
    ]

    self.wdg = QWidget(self.centralWidget)
    lout = QVBoxLayout(self.wdg)
    self.wdg.hide()

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

  def embedWindow(self, hwnd):
    wnd = QWindow.fromWinId(hwnd)
    self.wnd_container = self.createWindowContainer(wnd, self, Qt.FramelessWindowHint)
    self.wdg.layout().addWidget(self.wnd_container)
    self.wdg.show()

  def unembedWindow(self):
    # The embedded window is remove but the external process is still running.
    # The external process termination should be handled by it's owner (probably a bot)
    self.wnd_container.deleteLater()
    self.wnd_container = None
    self.wdg.hide()

  def resizeEmbbedWindow(self):
    parent_w, parent_h = self.centralWidget.width(), self.centralWidget.height()
    parent_x, parent_y = self.centralWidget.x(), self.centralWidget.y()
    wdg_w, wdg_h = parent_w // 1.5, parent_h // 1.5
    wdg_x, wdg_y = parent_x + (parent_w // 2) - (wdg_w // 2), parent_y + (parent_h // 2) - (wdg_h // 2)
    self.wdg.resize(wdg_w, wdg_h)
    self.wdg.move(wdg_x, wdg_y)

  def resizeEvent(self, event):
    self.animate(True)
    self.resizeEmbbedWindow() 

  def loadCharacters(self):
    for i in range(self.interval):
      for j in range(self.interval):
        self.labels[i][j].setText(config.CHARS[i][j])

  def resetCharacters(self):
    self.target = None
    self.autocomplete = False
    selected = self.labels[self.row][self.col].text()
    if selected == "␣":
      selected = " "
    # for testing
    # selected = "?"
    if selected == "⏎":
      # for testing
      self.ui_freeze.emit(True)
      if len(self.queries) == 0:
        self.send_query_signal.emit('2+2')
      else:
        self.send_query_signal.emit(self.queries.pop(0))
      # self.send_query_signal.emit(self.lblCmd.toPlainText())
    else:
      if len(selected) > 1:
        current_words = self.lblCmd.toPlainText().split(" ")
        current_words[-1] = selected
        self.insert_text(" ".join(current_words) + " ")
        # self.lblCmd.insertPlainText(" ".join(current_words) + " ")
      else:
        self.insert_text(self.lblCmd.toPlainText() + selected)
        # self.lblCmd.insertPlainText(self.lblCmd.toPlainText() + selected)
    self.row, self.col, self.interval = 0, 0, 8
    self.loadCharacters()
    self.animate(False)
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
      # if len(self.labels[self.row][self.col].text()) > 1 or result == 0:
      if self.autocomplete:
        QTimer.singleShot(1400, Qt.PreciseTimer, self.resetCharacters)
      else:
        self.ui_freeze.emit(True)
        self.autocomplete_signal.emit(self.lblCmd.toPlainText() + self.labels[self.row][self.col].text())

  def animate(self, flag = True):
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
          if len(x.text()) > 1:
            x.font_size = 1
          if self.interval == 8:
            # TODO: Use proper font size
            x.set_font_size(self.initial_font)
            x.setGeometry(QRect(label_width * j + shiftx, label_height * i + shifty, label_width, label_height))
          elif flag:
            easing_curve = QEasingCurve.InQuad
            animation = QPropertyAnimation(x, b'geometry', self)
            animation.setDuration(config.ANIMATION_DURATION)
            animation.setStartValue(x.geometry())
            if self.interval != 1:
              animation.setEndValue(QRect(label_width * j + shiftx , label_height * i + shifty , label_width, label_height))
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
            if len(x.text()) > 1:
              selected_size = min(label_width, label_height)/2
              l = QLabel()
              while True:
                l.setFont(QFont("MONO", selected_size))
                r = l.fontMetrics().boundingRect(x.text())
                if r.width() < x.width():
                  break
                selected_size //= 1.5
              print("selected: ", selected_size)
              print("bound: ", r.width())
              print("label: ", x.width())
              animation.setEndValue(selected_size)
            else:
              animation.setEndValue(min(label_width, label_height) / 2)

            animation.setEasingCurve(easing_curve)
            animation_group.addAnimation(animation)

      if flag:
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
    self.autocomplete = True
    if len(words) < 3:
      QTimer.singleShot(1400, Qt.PreciseTimer, self.resetCharacters)
    else:
      # words = [(self.labels[self.row][self.col].text(),0)] + words
      # should retain them, without any changes
      # self.row, self.col = 0, 0

      if self.target == 0:
        pass
      elif self.target ==1:
        self.col -= 1 
      elif self.target ==2:
        self.row -= 1 
      elif self.target ==3:
        self.row -= 1 
        self.col -= 1 

      idx = 0
      for i in range(2):
        for j in range(2):
          if 2*i + j != self.target:
            self.labels[self.row + i][self.col + j].setText(words[idx][0])
            idx += 1

      self.interval = 2
      self.animate(False)
      QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, lambda: self.ui_pause.emit(False))

  def insert_text(self, s):
    # self.lblCmd.moveCursor(QTextCursor.End)
    self.lblCmd.setPlainText(s)
    # self.lblCmd.textCursor().insertText(s)
    self.lblCmd.moveCursor(QTextCursor.End)
