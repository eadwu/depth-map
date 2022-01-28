import torch
import torch.nn as nn


class WeightedLoss(nn.Module):
    """Wrapper class for a simple merging of multiple losses."""
    def __init__(self, losses, weights):
        super().__init__()
        self.losses = nn.ModuleList(losses)
        self.weights = weights

    def forward(self, target, pred):
        weighted_loss = [
            f(target, pred) * w
            for f, w in zip(self.losses, self.weights)
        ]
        return torch.stack(weighted_loss, dim=0).sum(dim=0)
