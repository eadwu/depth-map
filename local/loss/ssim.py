from piqa import SSIM


class MaximumSSIMLoss(SSIM):
    """SSIM adjusted for minimization, not maximization."""
    def forward(self, target, pred):
        """
        If two images are exactly the same, then the SSIM score is 1.
          Backpropagation seeks to minimize, so this just conforms
          to it by making the ideal score 0.
        """
        return 1. - super().forward(target, pred)
