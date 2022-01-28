import torch
from piqa import SSIM
from torchvision.transforms.functional import adjust_sharpness


class MaximumSSIMLoss(SSIM):
    """SSIM adjusted for minimization, not maximization."""
    def forward(self, target, pred):
        """
        If two images are exactly the same, then the SSIM score is 1.
          Backpropagation seeks to minimize, so this just conforms
          to it by making the ideal score 0.
        """
        pred = torch.clip(pred, 0, self.value_range)
        target = adjust_sharpness(target, sharpness_factor=4)
        return 1. - super().forward(target, pred)
