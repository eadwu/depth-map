import os
import pandas as pd


def get_filelist(diode_root):
    filelist = []

    # Recursively read every file in the dataset
    for root, _, files in os.walk(diode_root):
        for file in files:
            filelist.append(os.path.join(root, file))

    # Sort to ensure that samples (image, depth map) are next to each other
    filelist.sort()
    return filelist


def format_filelist(filelist):
    # Divide into separate categories where each index corresponds to the
    #   image, depth map, and depth mask
    return {
        "image": [x for x in filelist if x.endswith(".png")],
        "depth": [x for x in filelist if x.endswith("_depth.npy")],
        "mask": [x for x in filelist if x.endswith("_depth_mask.npy")],
    }
