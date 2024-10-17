import numpy as np
import h5py
import bisect 

import config
import plotter
import contrast_max as cmax
import file_handler

def framework(x0, events, d_t):
  t0 = events[0][3] + 5000
  e_window: np.ndarray = event_window(events, t0, d_t)
  e_adjusted = np.array(list(map(lambda x: (x[0], x[1], x[2], x[3] - t0), e_window)))
  print(e_window)
  print(e_adjusted)


def get_initial_guess(t0, t, events):
  pass  

def event_window(events, t0, t): 
  i = bisect.bisect_left(events, t + t0, key=lambda x: x[3])
  j = bisect.bisect_right(events, t0, key=lambda x: x[3])
  return events[j: i]
  
if __name__ == "__main__":
#  plotter.plothdf5(config.RECORDING_PATH)
  fileHandler = file_handler.FileHandler(config.RECORDING_PATH)
  fileHandler.read_file()

  events = fileHandler.events
  framework(1, events, 4000)
  
  
   #first pass
