import concurrent.futures as cf
import time
from PyQt5.QtCore import QObject, pyqtSignal
from emokit.emotiv import Emotiv
from . import virtual, headset

def run(read, dev, collect_time):
  signals, quality =  read(dev, collect_time)
  return (signals, quality)

class Device(QObject):
  collect_signal = pyqtSignal(bool, tuple)

  def __init__(self, collect_time, callback=None, is_virtual=False, parent=None):
    super(Device, self).__init__(parent)
    self.callback = callback
    self.virtual = is_virtual
    self.future = None
    self.collect_time = collect_time
    self.read_func = virtual.read if self.virtual else headset.read
    self.dev = None if self.virtual else Emotiv()
    print("Device: open")

  def collect(self):
    print("Device: collect")
    self.collect_signal.emit(True, ())
    # We don't use python's 'with' block here
    # because it calls ProcessPoolExecutor.shutdown(True)
    # which is a blocking call thats freezes the main process
    self.exe = cf.ProcessPoolExecutor()
    self.future = self.exe.submit(run, self.read_func, self.dev, self.collect_time)
    self.future.add_done_callback(self.onCollectEvent)

  def onCollectEvent(self, future):
    self.collect_signal.emit(False, future.result())
  
  def stop(self):
    if self.future and self.future.running():
      print("Device: closing...")
      self.future.cancel()
      self.future = None
      self.exe.shutdown(True)
      print("Device: close")
