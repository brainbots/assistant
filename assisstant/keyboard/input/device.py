# -*- coding: utf-8 -*-
import concurrent.futures as cf
import time
from emokit.emotiv import Emotiv
import virtual, headset

def run(callback, collect_time, sleep_time):
  with Emotiv() as dev:
    while True:
      callback(collecting=True, data=None)
      data, _quality =  headset.read(dev, collect_time)
      callback(collecting=False, data=data)
      time.sleep(sleep_time)

def run_virt(callback, collect_time, sleep_time):
  while True:
    callback(collecting=True, data=None)
    data, _quality = virtual.read(None, collect_time)
    callback(collecting=False, data=data)
    time.sleep(sleep_time)

class Device(object):
  def __init__(self, collect_time, sleep_time, callback=None, virtual=False):
    self.callback = callback
    self.virtual = virtual
    self.future = None
    self.collect_time = collect_time
    self.sleep_time = sleep_time
    print("Device: open")

  def start(self):
    with cf.ProcessPoolExecutor() as exe:
      run_func = run_virt if self.virtual else run
      self.future = exe.submit(run_func, self.callback, collect_time, sleep_time)
      self.future.add_done_callback(self.exit)
      print("Device: start")

  def stop(self):
    if self.future:
      if self.future.cancel():
        self.future = None
      return self.future.running() 

  def exit(self, future):
    print("Device: close")

