import os
import torch
import random
import numpy as np
import matplotlib.pyplot as plt


def deterministic_environment(seed: int):
    """
    Attempts to provide as much of a reproducible environment as possible.

    Arguments:
        seed (int) - The number which to deterministically seed RNG
          generators
    """
    # Deterministic Randomness
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Deterministic Calculations
    torch.use_deterministic_algorithms(True)


def get_torch_device():
    """Determines which device to use with PyTorch."""
    return "cuda" if torch.cuda.is_available() else "cpu"


def visualize_depth_map(image, depth_map, output):
    """Visualizes three images in a row"""
    cmap = plt.cm.get_cmap("jet").copy()
    cmap.set_bad(color="black")

    fig, ax = plt.subplots(1, 3, figsize=(20, 20))
    ax[0].imshow(image)
    ax[1].imshow(depth_map, cmap=cmap)
    ax[2].imshow(output, cmap=cmap)
