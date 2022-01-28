import cv2
import numpy as np
from PIL import Image
from torch.utils.data import Dataset


class DIODEDataset(Dataset):
    """Class that can serve the contents of a diode dataset"""
    def __init__(self, data, image_transform=None, depth_transform=None):
        """
        Arguments:
            data (dict): Diode subset to use as the dataset
            transform (callable, optional): Optional preprocessing to be
                applied on a sample
        """
        self.image_transform = image_transform
        self.depth_transform = depth_transform
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path, depth_map, depth_mask = self.data.iloc[idx, :]

        # Load the image into memory
        image = Image.open(image_path)

        # Load the depth information to memory
        depth_map = np.load(depth_map)

        # Load the depth mask into memory
        depth_mask = np.load(depth_mask)
        # Boolean array which signifies if information came from the sensor
        depth_mask = depth_mask > 0

        if self.image_transform is not None:
            image = self.image_transform(image)

        if self.depth_transform is not None:
            depth_map = self.depth_transform(depth_map)

        return {
            "input": image,
            "target": depth_map,
            "mask": depth_mask
        }
