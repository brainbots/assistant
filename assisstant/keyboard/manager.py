from PyQt5.QtCore import Qt, QObject, QTimer, pyqtSignal
from keyboard.input import device
from keyboard import config
from keyboard.classification import cca
from random import randint

class Manager(QObject):
  flash_signal = pyqtSignal(bool)
  update_signal = pyqtSignal(int)

  def __init__(self, is_virtual, parent=None):
    super(Manager, self).__init__(parent)
    self.is_virtual = is_virtual
    self.freeze = False
    self.device = device.Device(callback=self.device_update,
                                collect_time=config.TIME_FLASH_SEC, is_virtual=self.is_virtual)
    self.device.collect_signal.connect(self.device_update)
    self.paused = False

  def pause_handler(self, paused):
    self.paused = paused
    print("Paused: ", paused)
    if paused or self.freeze:
      self.stop()
    else:
      self.start()

  def freeze_handler(self):
    self.freeze = True

  def start(self):
    if not self.paused:
      #QTimer.singleShot(1000, Qt.PreciseTimer, self.device.collect)
      self.device.collect()

  def stop(self):
    self.device.stop()

  def device_update(self, collecting, data=None):
    if self.freeze:
      return

    self.flash_signal.emit(collecting)
    if not collecting:
      sample, _quality = data
      if self.is_virtual:
        result = randint(0, 3)
      else:
        result = cca.classify(sample, config.FREQ, config.TIME_FLASH_SEC) - 1
      self.update_signal.emit(result)
      if not self.paused:
        QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, self.device.collect)

