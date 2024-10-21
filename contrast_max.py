import numpy as np
import scipy.optimize
import scipy.linalg as sla
import bisect
import config


def get_cross_matrix(omega: np.ndarray) -> np.matrix:
    """ returns the skew symmetric matrix related to the cross product with omega
        omega x b is equivalent to Ab where A is the related matrix
    Args:
        omega (np.ndarray): 3d np array of rotation

    Returns:
        _type_: _description_
    """
    return np.matrix(
        [[0, -omega[2],  omega[1]],
         [omega[2], 0, -omega[0]],
            [omega[1], omega[2], 0]])


def rot_warp_pixel(e: np.ndarray, t: float, theta: np.ndarray) -> np.ndarray:

    x_bar = np.transpose(np.array([e[0], e[1], 1]))
    theta_hat = get_cross_matrix(theta)

    res = np.matmul(sla.expm(theta_hat * t), x_bar)
    res = res.astype(int)
    return res.astype(int)


def minimize(f, events, initial_guess):
    return scipy.optimize.minimize(f, initial_guess, args=(events), method="Nelder-Mead")


def event_image(events):
    print(events[-1])
    img = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH))
    for event in events:
        # the actual formula per pixel is b_k * s(x - x_k) with s = dirac delta funciton but no
        # we can also use the gaussian with multivar normal dist with mu = x_k (and sigma = 1?)
        event = event.astype(int)
        if 0 <= event[0] <= config.IMAGE_WIDTH and 0 <= event[1] <= config.IMAGE_HEIGHT:
            img[event[1]][event[0]] += event[2]
    return img


def compute_variance(img, events):
    n_p = len(events)
    mean = 1 / n_p * np.sum(img)
    variance = 1 / n_p * np.sum(np.multiply(img - mean, img - mean))
    return variance


def event_window(events, t0, t):
    i = bisect.bisect_left(events, t + t0, key=lambda x: x[3])
    j = bisect.bisect_right(events, t0, key=lambda x: x[3])
    return np.array(list(map(lambda x: np.array([x[0], x[1], x[2], x[3]], dtype="float64"), events[j: i])))


def get_initial_guess(_events):
    return np.array([0., 0., 0.]).flatten()
