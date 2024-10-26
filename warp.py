import numpy as np
import scipy.optimize
import scipy.linalg as sla
import bisect
import config


def get_translation_matrix(t: np.ndarray) -> np.ndarray:
    return np.array([
        [1, 0, t[0]],
        [0, 1, t[1]],
        [0, 0, 1]
    ])


def get_rotation_matrix(w: np.ndarray) -> np.ndarray:
    r = w[0]
    p = w[1]
    y = w[2]

    yaw_mat = np.array([
        [np.cos(y), -np.sin(y), 0],
        [np.sin(y),  np.cos(y), 0],
        [0, 0, 1]
    ])

    pitch_mat = np.array([
        [np.cos(p), 0,  np.sin(p)],
        [0, 1, 0],
        [-np.sin(p), 0, np.cos(p)],
    ])

    roll_mat = np.array([
        [1, 0, 0],
        [0, np.cos(r), -np.sin(r)],
        [0, np.sin(r),  np.cos(r)],
    ])

    return np.matmul(yaw_mat, np.matmul(pitch_mat, roll_mat))


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
         [omega[2], 0,  -omega[0]],
         [omega[1], omega[2], 0]])


def rot_warp_pixel(e: np.ndarray, t: float, theta: np.ndarray) -> np.ndarray:

    x_bar = np.transpose(np.array([e[0], e[1], 1]))
    theta_hat = get_rotation_matrix(np.multiply(theta, t))
    trans = get_translation_matrix(
        [config.IMAGE_WIDTH // 2, config.IMAGE_HEIGHT // 2])

    f_mat = np.matmul(np.linalg.inv(trans), np.matmul(theta_hat, trans))

    res = np.matmul(f_mat, x_bar)
    return res.astype(int)


def vel_warp_pixel(e: np.ndarray, t: float, v: np.ndarray) -> np.ndarray:
    x_bar = np.array(e[0], e[1]) + v

    return x_bar.astype(int)


def event_image(events):
    img = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH))
    for event in events:
        # the actual formula per pixel is b_k * s(x - x_k) with s = dirac delta funciton but no
        # we can also use the gaussian with multivar normal dist with mu = x_k (and sigma = 1?)
        event = event.astype(int)
        if 0 <= event[0] < config.IMAGE_WIDTH and 0 <= event[1] < config.IMAGE_HEIGHT:
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
    return np.array(list(map(lambda x: np.array([x[0], x[1], x[2], x[3] - t0], dtype="float64"), events[j: i])))


def get_initial_guess(_events):
    return np.array([0.00, 0.00000, 0.0000]).flatten()
