import os
os.environ['HDF5_PLUGIN_PATH'] = "./hdf5_ecf/"
import numpy as np
import h5py
import hdf5plugin 

import config

def plothdf5(filepath):
  #
  # hdf5 file format : {
    # CD: {events: dataset, indexes: dataset}, 
    # EXT_TRIGGER : {events: dataset, indexes: indexes}}
  #
  with h5py.File("./data/recording.hdf5", 'r') as hf_in:
    dset: h5py.Dataset = hf_in['CD']['events']
    positives = [] 
    for event in dset[ :]:
      if event[2] == 1:
        positives.append(True)
      else:
        positives.append(False)
    
    # with h5py.File(filepath, 'r') as f:

  #   events: np.ndarray = f["CD"]["events"]
  
  #   total_events = len(events)
  #   duration = (events[total_events - 1]['t'] - events[0]['t']) / 10**6
  #   print(events[:100])    
  #   print(total_events, duration)


