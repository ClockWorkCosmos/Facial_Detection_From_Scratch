import os
import random
import shutil
import cv2

from albumentations import (
    HorizontalFlip,
    VerticalFlip,
    RandomBrightnessContrast,
    Rotate,
    RGBShift,
)

input_folder = "database"
augmented_folder = "database"
dataset_folder = "database"

os.makedirs(augmented_folder, exist_ok=True)
os.makedirs(dataset_folder, exist_ok=True)

transformations = [
    HorizontalFlip(),
    VerticalFlip(),
    RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2),
    Rotate(limit=45),
    RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15),
]

for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    image = cv2.imread(file_path)
    for i, transformation in enumerate(transformations):
        augmented = transformation(image=image)
        new_file_name = file_name.split(".")[0] + f"augmented{i}.png"
        new_file_path = os.path.join(augmented_folder, new_file_name)
        cv2.imwrite(new_file_path, augmented["image"])