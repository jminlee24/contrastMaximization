import numpy as np
import scipy.optimize
import scipy.linalg as sla
import config

def get_cross_matrix(omega : np.ndarray) -> np.matrix:
  """ returns the skew symmetric matrix related to the cross product with omega
      omega x b is equivalent to Ab where A is the related matrix
  Args:
      omega (np.ndarray): 3d np array of rotation 

  Returns:
      _type_: _description_
  """
  return np.matrix(
    [[0      ,-omega[2],  omega[1] ],
    [omega[2], 0       , -omega[0]],
    [omega[1], omega[2], 0]])

def rot_warp_pixel(e: np.ndarray, t : float, theta: np.ndarray) -> np.ndarray:
  
  x_bar = np.transpose(np.array([e[0], e[1], 1]))
  theta_hat = get_cross_matrix(theta)

  return np.matmul(sla.expm(theta_hat * t), x_bar)

def maximize(f, events, initial_guess):
  return scipy.optimize.minimize(f, initial_guess, args=(events))

def event_image(events):
  img = np.zeros((config.IMAGE_HEIGHT, config.IMAGE_WIDTH))
  for event in events:
# the actual formula per pixel is b_k * s(x - x_k) with s = dirac delta funciton but no
# we can also use the gaussian with multivar normal dist with mu = x_k (and sigma = 1?)
    img[event[0]][event[1]] += event[2] 
    
def compute_variance(img):
  n_p = config.IMAGE_HEIGHT * config.IMAGE_WIDTH
  mean = 1 / n_p* np.sum(img)
  variance = 1/ n_p* np.sum(np.multiply(img - mean, img - mean))
  return variance

