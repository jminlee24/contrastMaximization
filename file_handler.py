import os
import numpy as np
import h5py 
import hdf5plugin

class FileHandler:
  def __init__(self, filepath ):
    self.events : np.ndarray = []
    self.filepath = filepath
    self.filetype = os.path.splitext(filepath)[1]

  def handle_hdf5(self):
    with h5py.File(self.filepath, "r") as hf:
      dset: h5py.Dataset = hf["CD"]["events"]
      self.events = np.array(dset[:])

  def handle_txt(self ):
    with open(self.filepath, 'r') as f:
      lines = f.readlines()
      res = map(lambda x : x.rstrip().split(' '), lines)
      res = map(lambda x : [int(x[1]), int(x[2]), int(x[3]), int(float(x[0]) * 1000)], res )
      self.events = np.array(list(res)) 

  def read_file(self ):
    if self.filetype == ".hdf5":
      self.handle_hdf5()
    elif self.filetype == ".txt":
      self.handle_txt()
    else:
      raise OSError("Not a valid file type")
 
  def filter_events(self, filter):
    filter_array = []
    for event in self.events[:10]:
      filter_array.append(filter(event))
    return self.events[:10][filter_array]
  
  def print_events(self ):
    for event in self.events[-100:]:
      print(event )
  