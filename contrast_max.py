import scipy

import config
import warp
import file_handler
import plotter


class ContrastMaximizer:
    def __init__(self, filepath, h=-1):
        self.file_handler = file_handler.FileHandler(filepath)
        self.file_handler.read_file(h=h)
        self.filtered_events = self.file_handler.filter_events(
            lambda x: x[2] == 1)
        self.plotter = plotter.Plotter()
        self.x0 = []
        self.t0 = 0

    @staticmethod
    def create_image(events):
        img = warp.event_image(events)
        return img

    @staticmethod
    def single_pass(x0, events):
        warped_events = [warp.rot_warp_pixel(
            event, event[3], x0) for event in events]
        img = warp.event_image(warped_events)
        return -warp.compute_variance(img, warped_events)

    def maximize_variance(self, t0):
        self.t0 = t0
        events = warp.event_window(
            self.filtered_events, t0, config.TIME_WINDOW)
        x0 = warp.get_initial_guess(events)
        res = scipy.optimize.minimize(
            ContrastMaximizer.single_pass, x0=x0, args=events, method="Nelder-Mead", tol=.001)

        self.x0 = res.x
        return res

    def plot_images(self):
        events = warp.event_window(
            self.filtered_events, self.t0, config.TIME_WINDOW)

        warped_events = [warp.rot_warp_pixel(
            event, event[3], self.x0) for event in events]

        warped_img = self.create_image(warped_events)
        img = self.create_image(events)

        self.plotter.plot_image(warped_img, title="warped events")
        self.plotter.plot_image(img, title="original events")
        self.plotter.plot_events(self.file_handler.events, title="events")

        self.plotter.show()
