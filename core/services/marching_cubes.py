"""
This module contains marching cube functionality.
"""

import logging
from typing import Tuple

import numpy as np
from skimage import measure

from scipy.ndimage import zoom

def downsample_volume(volume_data: np.ndarray, factor: int) -> np.ndarray:
    """
    Downsample the volume data by a specified factor.

    Parameters:
        volume_data (np.ndarray): The input volume data as a 3D NumPy array.
        factor (int): The downsampling factor. A factor of 2 means halving the resolution.

    Returns:
        np.ndarray: The downsampled volume data as a new 3D NumPy array.
    """
    return zoom(volume_data, 1 / factor, order=1)

def generate_mesh(
    image_data: np.ndarray, threshold=300, step_size=2
) -> Tuple[np.array, np.array, np.array]:
    logging.info("Generating mesh")
    logging.info("Marching cubes: Transposing surface")

    # For NIfTI with 5D shape (time etc.); most NIfTI comes in 3D anyway
    if len(image_data.shape) == 5:
        image_data = image_data[:, :, :, 0, 0]
    volume = image_data.transpose((2, 1, 0))
    
    volume = downsample_volume(volume, 2)

    logging.info("Marching cubes: Calculating surface...")
    verts, faces, norm, val = measure.marching_cubes_lewiner(
        volume, threshold, step_size=step_size, allow_degenerate=True
    )

    return verts, faces, norm

def seperate_segmentation(data: np.ndarray, unique_values: list = []) -> np.ndarray:
        """
        Seperate unique values into a new dimension. If no unique values are
        given, np.unique() will be used.
        """
        if not unique_values:
            unique_values = np.unique(data)
        result = np.zeros((len(unique_values),) + data.shape)
        for i, value in enumerate(unique_values):
            temp = np.array(data)
            temp[temp != value] = 0
            result[i] = temp
        return result
