import matplotlib.pyplot as plt
import numpy as np

import config


class Plotter:

    def plot_events(self, events, title="no title", start=0, end=9000):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_title(title)
        xs = events[:, 0]
        ys = events[:, 3]
        zs = events[:, 1]
        ax.scatter(xs, ys, zs, s=.01, marker=".", )

    def plot_image(self, img, title='no title'):
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_title(title)
        plt.gca().invert_yaxis()
        # img = img / np.max(img)
        img = np.clip(img, 0, 1)
        ax.imshow(img, cmap="gray")

    def show(self):
        plt.show()
