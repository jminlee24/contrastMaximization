import numpy as np
import h5py
import bisect
import scipy

import config
import plotter
import visualization
import contrast_max as cmax
import file_handler


def single_pass(x0, events):
    warped_events = []
    for event in events:
        warped_events.append(cmax.rot_warp_pixel(event, event[3], x0))
    e_img = cmax.event_image(warped_events)
    return -cmax.compute_variance(e_img, warped_events)


def framework(events, d_t):
    t0 = events[0][3] + 500
    e_window: np.ndarray = cmax.event_window(events, t0, d_t)
    e_adjusted = np.array(
        list(map(lambda x: (x[0], x[1], x[2], x[3] - t0), e_window)))
    x0 = cmax.get_initial_guess(e_adjusted)
    res = scipy.optimize.minimize(single_pass, x0=x0, args=e_adjusted, method="CG")
    print(res)
    warped_events = [cmax.rot_warp_pixel(event, event[3], res.x)
                 for event in e_adjusted]
    warped_img = cmax.event_image(warped_events)
    img = cmax.event_image(e_adjusted)
    plotter = visualization.Plotter()
    plotter.plot_image(img, "normal")
    plotter.plot_image(warped_img, "warped!") 
    plotter.show()

if __name__ == "__main__":
    #  plotter.plothdf5(config.RECORDING_PATH)
    fileHandler = file_handler.FileHandler(config.TEST_RECORDING_PATH)
    fileHandler.read_file(h=30000)

    events = fileHandler.events
    framework(events, 500)

    # first pass
