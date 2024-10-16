import numpy as np
import h5py

import config
import plotter
import contrast_max as cmax

def framework(x0, events):
  pass

if __name__ == "__main__":
  plotter.plothdf5(config.RECORDING_PATH)

  with h5py.File(config.RECORDING_PATH, "r") as f:
    dset = f["CD"]
    events = dset["events"] # type: ignore
    #first pass
