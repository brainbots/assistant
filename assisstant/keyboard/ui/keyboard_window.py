from math import ceil
from PyQt5.QtCore import QRect, Qt, QTimer, pyqtProperty, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QWindow, QTextCursor
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QLayout
from pymouse import PyMouse

import settings as config
from .keyboard_ui import Ui_KeyboardWindow
from .components import CustomLabel

class KeyboardWindow(QMainWindow, Ui_KeyboardWindow):
  ui_reloaded_signal = pyqtSignal(str)

  def __init__(self):
    super(KeyboardWindow, self).__init__()
    self.chars = config.CHARS
    self.commands = []
    self.max_interval = len(self.chars[0])
    self.embedded_mode = False
    self.initial_font = config.INITIAL_FONT
    self.setupUi(self)
    self.target = None
    self.autocomplete = False
    self.boxes = [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
    self.mouse = PyMouse()

    self.geometries = [None, None, None, None]
    self.history = []

    self.wdg = QWidget()
    lout = QVBoxLayout(self.wdg)
    lout.setSizeConstraint(QLayout.SetDefaultConstraint)
    lout.setContentsMargins(0, 0, 0, 0)
    lout.setSpacing(0)

    for index, box in enumerate(self.boxes):
      box.setFreq(config.FREQ[index])
      box.setColor(config.COLOR[index])

    # TODO: Create label for the undo box

    self.labels = [list()]
    self.row, self.col, self.interval = 0, 0, self.max_interval
    
    for i in range(4):
      label = CustomLabel(self.centralWidget, self.initial_font)
      label.setStyleSheet("QLabel { color : rgba(255, 255, 255, 0.5);}")
      label.resize(100, 100)
      label.setAttribute(Qt.WA_TranslucentBackground)
      label.setAlignment(Qt.AlignCenter)
      label.hide()
      self.commands.append(label)
    
    for i in range(self.interval):
      self.labels.append(list())
      for j in range(self.interval):
        # TODO: Use proper font size
        label = CustomLabel(self.centralWidget, self.initial_font)
        label.setText(self.chars[i][j])
        label.setStyleSheet("QLabel { color : rgba(255, 255, 255, 0.5); }")
        label.setAttribute(Qt.WA_TranslucentBackground)
        label.setAlignment(Qt.AlignCenter)
        label.show()
        self.labels[i].append(label)

  def execKeyboardEvent(self, fn):
    x_dim, y_dim = self.mouse.screen_size()
    self.mouse.move(x_dim // 2, y_dim // 2)
    fn()

  def embedWindow(self, hwnd, labels):
    wnd = QWindow.fromWinId(hwnd)
    self.wnd_container = self.createWindowContainer(wnd, self.wdg, Qt.FramelessWindowHint)
    self.wdg.layout().addWidget(self.wnd_container)
    self.wnd = wnd

    self.hideChars()
    
    for i in range(len(self.commands)):
      self.commands[i].setText(labels[i])
      self.geometries[i] = self.boxes[i].geometry()
      self.commands[i].show()

    self.embedded_mode = True
    self.resizeEmbbedWindow()
    self.update()
    self.wdg.setParent(self)
    self.wdg.show()

  def unembedWindow(self):
    # The embedded window is remove but the external process is still running.
    # The external process termination should be handled by it's owner (probably a bot)
    self.wdg.hide()
    for i in range(len(self.commands)):
      self.commands[i].setText("")
      self.boxes[i].setGeometry(self.geometries[i])
      self.commands[i].hide()

    self.embedded_mode = False
    #TODO: this causes layout freeze
    #self.resetCharacters()
    self.wdg.layout().removeWidget(self.wnd_container)
    self.wdg.setParent(None)
    self.wnd_container.deleteLater()
    self.wnd_container.setParent(None)

  def resizeEmbbedWindow(self):
    parent_w, parent_h = self.centralWidget.width(), self.centralWidget.height()
    parent_x, parent_y = self.centralWidget.x(), self.centralWidget.y()
    wdg_w, wdg_h = parent_w - 200, parent_h - 100
    wdg_x, wdg_y = parent_x + (parent_w // 2) - (wdg_w // 2), parent_y
    self.wdg.resize(wdg_w, wdg_h)
    self.wdg.move(wdg_x, wdg_y)

    if not self.embedded_mode:
      return

    grid_rect = self.gridLayout.geometry()
    grid_w, grid_h = grid_rect.width(), grid_rect.height()
    grid_x, grid_y = grid_rect.x(), grid_rect.y()

    for i in range(4):
      label = self.commands[i]
      if i == 0:
        label.move(grid_x, grid_y)
      elif i == 1:
        label.move(grid_x + grid_w - label.width(), grid_y)
      elif i == 2:
        label.move(grid_x, grid_y + grid_h - label.height())
      elif i == 3:
        label.move(grid_x + grid_w - label.width(), grid_y + grid_h - label.height())

      self.boxes[i].setGeometry(label.geometry())
 

  def resizeEvent(self, event):
    self.animate(True)
    self.resizeEmbbedWindow() 
    self.resize_timer()

  def loadCharacters(self):
    for i in range(self.interval):
      for j in range(self.interval):
        self.labels[i][j].setText(self.chars[i][j])

  def resetCharacters(self):
    self.target = None
    self.autocomplete = False
    selected = self.labels[self.row][self.col].text()
    if selected == "⌫":
      self.undo_insert()
    elif selected == "⏎":
      print("ENTER!")
    else:
      s = ""
      if selected == "␣":
        selected = " "

      if len(selected) > 1:
        current_words = self.lblCmd.toPlainText().split(" ")
        current_words[-1] = selected
        s = " ".join(current_words) + " "
        self.update_input(s)
      else:
        s = self.lblCmd.toPlainText() + selected
        self.update_input(s)
      self.history.append(s)
    self.row, self.col, self.interval = 0, 0, self.max_interval
    self.loadCharacters()
    self.animate(False)
    self.ui_reloaded_signal.emit(selected)

  def update_handler(self, result):
    if self.embedded_mode:
        return None
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
      # self.ui_pause.emit(True)
      self.target = result
      if self.autocomplete:
        QTimer.singleShot(1400, Qt.PreciseTimer, self.resetCharacters)
      return self.labels[self.row][self.col].text(), self.autocomplete
    else:
      return False, False


  def hideChars(self):
    for i in range(self.max_interval):
      for j in range(self.max_interval):
        self.labels[i][j].hide()

  # reposition timer
  def resize_timer(self):
    parent_w, parent_h = self.gridLayout.geometry().width(), self.gridLayout.geometry().height()
    parent_x, parent_y = self.gridLayout.geometry().x(), self.gridLayout.geometry().y()
    size = self.timer_lbl.sizeHint()
    wdg_w, wdg_h = size.width(), size.height()
    wdg_x, wdg_y = parent_x + (parent_w // 2) - (wdg_w // 2), parent_y + (parent_h // 2) - (wdg_h // 2)

    self.timer_lbl.resize(wdg_w, wdg_h)
    self.timer_lbl.move(wdg_x, wdg_y)

  def show_timer(self):
    self.timer_lbl.show()
    n = self.startTimer(1000, Qt.PreciseTimer)
    self.countdown = config.TIME_REST_SEC
    self.timer_lbl.setText(str(self.countdown))

  def timerEvent(self, event):
    self.countdown -= 1
    self.timer_lbl.setText(str(self.countdown))
    if self.countdown == 0:
      self.timer_lbl.hide()
      self.killTimer(event.timerId())


  def animate(self, flag = True):
    if self.embedded_mode:
      return
    label_width = (self.gridLayout.geometry().width() - 2 * config.GRIDLAYOUT_MARGIN - config.GRIDLAYOUT_SPACING) // self.interval
    label_height = (self.gridLayout.geometry().height() - 2 * config.GRIDLAYOUT_MARGIN - config.GRIDLAYOUT_SPACING) // self.interval

    # TODO: Don't hide the labels that will remain
    self.hideChars()

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
          # start the font animation of suggested words from small size
          # the interval check prevents it from working on the following animation
          if len(x.text()) > 1 and self.interval == 2:
            x.font_size = 1
          if self.interval == self.max_interval:
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
              animation.setEndValue(selected_size)
            else:
              animation.setEndValue(min(label_width, label_height) / 2)

            animation.setEasingCurve(easing_curve)
            animation_group.addAnimation(animation)

      if flag:
        animation_group.start()

  def flash_handler(self, value):
    if self.interval == 1:
      return
    if value:
      print("Flash: on")
      for box in self.boxes:
        box.startFlashing()
    else:
      print("Flash: off")
      for box in self.boxes:
        box.stopFlashing()

  def receive_predicted_words(self, words):
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
            self.labels[self.row + i][self.col + j].setText(words[idx])
            idx += 1

      self.interval = 2
      self.animate(False)
      self.ui_reloaded_signal.emit("")
      # QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, lambda: self.ui_pause.emit(False))

  def get_input(self):
    return self.lblCmd.toPlainText()

  def update_input(self, s):
    # self.lblCmd.moveCursor(QTextCursor.End)
    self.lblCmd.setText(s)
    # self.lblCmd.textCursor().insertText(s)
    self.lblCmd.moveCursor(QTextCursor.End)

  def update_prompt(self, s):
    self.undo.setText(s)

  def undo_insert(self):
    if len(self.history) > 0:
      self.history.pop()
      s = self.history[-1] if len(self.history) > 0 else ''
      print("state: ", s)
      self.update_input(s)
