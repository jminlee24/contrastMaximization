import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

import file_handler
import config

class Plotter:
  def __init__(self, data: np.ndarray):
    self.fig = plt.figure()
    self.ax3 = self.fig.add_subplot(projection="3d")
    self.ax2 = self.fig.add_subplot(projection="2d")

    self.data = data
  
  def plot_events(self):
    xs = self.data[:,0]
    ys = self.data[:,3]
    zs = self.data[:,1]
    self.ax.scatter(xs, ys, zs, marker=".", s=.01)
    plt.show()
  
  def plot_image(self):
    

fileHandler = file_handler.FileHandler(config.TEST_RECORDING_PATH)
fileHandler.read_file()

events = fileHandler.events
events = fileHandler.filter_events(lambda x : x[2] == 1)

print(events)

plotter = Plotter(events[:100000])
plotter.plot_events()

    