import numpy as np
import h5py
import bisect 
import scipy

import config
import plotter
import contrast_max as cmax
import file_handler

def single_pass(x0, events):
  warped_events = []
  for event in events:
    warped_events.append(cmax.rot_warp_pixel(event ,event[3], x0))
  e_img = cmax.event_image(warped_events)
  return cmax.compute_variance(e_img)

def framework(events, d_t):
  t0 = events[0][3] + 5000
  e_window: np.ndarray = event_window(events, t0, d_t)
  e_adjusted = np.array(list(map(lambda x: (x[0], x[1], x[2], x[3] - t0), e_window)))
  x0 = get_initial_guess(e_adjusted)
  print(scipy.optimize.minimize(single_pass, x0=x0, args=e_adjusted))

def get_initial_guess(_events):
  return np.array([0.2, 0.2, 0.2]).flatten()


def event_window(events, t0, t): 
  i = bisect.bisect_left(events, t + t0, key=lambda x: x[3])
  j = bisect.bisect_right(events, t0, key=lambda x: x[3])
  return np.array(list(map(lambda x: np.array([x[0], x[1], x[2], x[3]], dtype="float64"), events[j: i])))
  
if __name__ == "__main__":
#  plotter.plothdf5(config.RECORDING_PATH)
  fileHandler = file_handler.FileHandler(config.RECORDING_PATH)
  fileHandler.read_file()

  events = fileHandler.events
  framework(events, 4000)
  
  
   #first pass
