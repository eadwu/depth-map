import numpy as np

class DepthMask(object):
    def __init__(self, mask):
        self.mask = mask

    def __call__(self, depth_map):
        # Include mask information into depth map
        return np.ma.masked_where(~depth_mask, depth_map)
