import torch
from torchvision.transforms import Normalize


class ClipMaxDepth(object):
    # Clip depth values to a maximum of 300 or the 99th percentile
    def __init__(self, max_depth, clip_percentile=99):
        self.max_depth = max_depth

    def __call__(self, x):
        # max_depth = min(300, np.percentile(depth_map, 99))
        return torch.clip(x, 1e-6, self.max_depth)


class ZScoreNormalization(object):
    def __init__(self):
        pass

    def __call__(self, x):
        """Normalizes along the width and height dimensions"""
        mean, std = torch.mean(x, dim=(1, 2)), torch.std(x, dim=(1, 2))
        return Normalize(mean=mean, std=std)(x)


class MinMaxScaler(object):
    def __init__(self, min=0., max=1.):
        self.min = min
        self.max = max
        self.scaled_range = max - min

    def __call__(self, x):
        x_max = torch.max(x)
        x_min = torch.min(x)
        feature_range = x_max - x_min

        x = x - x_min
        x = x / feature_range
        return x * self.scaled_range + self.min
