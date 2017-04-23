from PyQt5.QtCore import Qt, QObject, QTimer, pyqtSignal
from keyboard.input import device
from keyboard import config

class Manager(QObject):
  flash_signal = pyqtSignal(bool)

  def __init__(self, parent=None):
    super(Manager, self).__init__(parent)
    self.device = device.Device(callback=self.device_update, collect_time=config.TIME_FLASH_SEC, is_virtual=True)
    self.device.collect_signal.connect(self.device_update)

  def start(self):
    self.device.collect()

  def stop(self):
    self.device.stop()

  def device_update(self, collecting, data=None):
    self.flash_signal.emit(collecting)
    if not collecting:
      signals, _quality = data
      QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, self.device.collect)
 
