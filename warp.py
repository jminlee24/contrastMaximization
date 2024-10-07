import numpy as np
import scipy.linalg as sla 

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
  
  x_bar = np.transpose(np.array(e[0], e[1], 1))
  theta_hat = get_cross_matrix(theta)

  return np.matmul(sla.expm(theta_hat * t), x_bar)
