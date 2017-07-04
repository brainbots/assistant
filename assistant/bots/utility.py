import subprocess

# criteria: dictionary that has key/values to match against.
# e.g. {"wm_class": "Navigator.Firefox"}
def getWindow(criteria):
  windows = getAllWindows()
  for window in windows:
    if criteria.items() <= window.items():
      print(window)
      return window
  return None


def getAllWindows():
  windows = []
  with subprocess.Popen(["wmctrl", "-l", "-p", "-x"], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
      tokens = line.split()
      windows.append({"hwnd": int(tokens[0], 16), "workspace": int(tokens[1]), "pid": int(tokens[2]), "wm_class": tokens[3], "title": " ".join(tokens[5:])})
  return windows
