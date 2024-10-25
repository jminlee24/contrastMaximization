import matplotlib.pyplot as plt
import numpy as np

import file_handler
import contrast_max as cm
import config


class Plotter:

    def plot_events(self, events, title="no title"):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_title(title)
        xs = events[:, 0]
        ys = events[:, 3]
        zs = events[:, 1]
        ax.scatter(xs, ys, zs, marker=".", s=.01)

    def plot_image(self, img, title='no title'):
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_title(title)
        ax.imshow(img, vmin=-np.abs(img).max(), vmax=np.abs(img).max(), cmap="gray")

    def show(self):
        plt.show()

if __name__=="__main__":

    fileHandler = file_handler.FileHandler(config.TEST_RECORDING_PATH)
    fileHandler.read_file(h=100000)

    events = fileHandler.events
    events = fileHandler.filter_events(lambda x: x[2] == 1)

    plotter = Plotter()
    plotter.plot_events(events[:5000])

    trimmed_events = cm.event_window(events, 500, 500)
    x0 = cm.get_initial_guess(0)

    plotter.plot_events(trimmed_events, "normal")

    warped_events = [cm.rot_warp_pixel(event, event[3], [0.0000001, 0.00000001, 0.0001])
                    for event in trimmed_events]
    warped_img = cm.event_image(warped_events)
    img = cm.event_image(trimmed_events)
    print(cm.compute_variance(warped_img, img))

    plotter.plot_image(warped_img, "warped")
    plt.gca().invert_yaxis()
    plotter.plot_image(img, "normal")
    plt.gca().invert_yaxis()

    plt.show()
