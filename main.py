import numpy as np
import h5py

import config
import plotter
import contrast_max as cmax
import file_handler

def framework(x0, events):
  pass

if __name__ == "__main__":
#  plotter.plothdf5(config.RECORDING_PATH)
  fileHandler = file_handler.FileHandler(config.TEST_RECORDING_PATH)
  fileHandler.read_file()
  print(fileHandler.events)
  
   #first pass
