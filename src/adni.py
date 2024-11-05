import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import nibabel as nib
import os
import h5py
import pandas as pd
import torchio as tio
import monai.transforms as montrans
from typing import List, Tuple
import logging

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

DIAGNOSIS_MAP = {"CN": 0, "MCI": 1, "FTD": 1, "Dementia": 2, 'AD': 2}
DIAGNOSIS_MAP_binary = {"CN": 0, "Dementia": 1, 'AD': 1}
LOG = logging.getLogger(__name__)

def get_image_transform(is_training: bool):
    img_transforms = [
        tio.RescaleIntensity(out_min_max=(0, 1)),
        tio.CropOrPad((128, 128, 128))
    ]

    if is_training:
        randomAffineWithRot = tio.RandomAffine(
            scales=0.2,
            degrees=90,  # +-90 degree in each dimension
            translation=8,  # +-8 pixels offset in each dimension.
            image_interpolation="linear",
            default_pad_value="otsu",
            p=0.5,
        )
        img_transforms.append(randomAffineWithRot)
    
    img_transform = montrans.Compose(img_transforms)
    return img_transform

class AdniDataset(Dataset):
    def __init__(self, 
                path: str, 
                is_training: bool, 
                out_class_num: int, 
                with_mri: bool, 
                with_pet: bool,
                ):
        self.path = path
        if with_mri is True and with_pet is True:
            self.transforms = [
                get_image_transform(is_training),
                get_image_transform(is_training),
            ]
        elif with_mri is True or with_pet is True:
            self.transforms = [
                get_image_transform(is_training)
            ]
        else:
            print('Please choose with mri or with pet')

        self.out_class_num = out_class_num
        self.with_mri = with_mri
        self.with_pet = with_pet

        self._load()

    def _load(self):
        image_data = []
        diagnosis = []
        rid = []

        with h5py.File(self.path, mode='r') as file:
            for name, group in file.items():
                if name == "stats":
                    continue

                if self.out_class_num == 2 and group.attrs['DX'] == "MCI":
                    continue

                pet_data = group['PET/FDG/data'][:]
                pet_data = np.nan_to_num(pet_data, copy=False)
                mri_data = group['MRI/T1/data'][:]
                
                if self.with_mri is True and self.with_pet is True:
                    image_data.append(
                        ( 
                            mri_data[np.newaxis],
                            pet_data[np.newaxis],
                        )
                    )
                elif self.with_mri is True and self.with_pet is False:
                    image_data.append(                           
                            mri_data[np.newaxis]
                        )
                    
                elif self.with_mri is False and self.with_pet is True:
                    image_data.append(
                            pet_data[np.newaxis]                            
                        )
                    
                else:
                    continue

                diagnosis.append(group.attrs['DX'])    
                rid.append(group.attrs['RID'])
                                            
        LOG.info("DATASET: %s", self.path)
        LOG.info("SAMPLES: %d", len(image_data))

        print("DATASET: ", self.path)
        print("SAMPLES: ", len(image_data))

        labels, counts = np.unique(diagnosis, return_counts=True)
        LOG.info("Classes: %s", pd.Series(counts, index=labels))

        print("Classes: ", pd.Series(counts, index=labels))
        
        self._image_data = image_data

        if self.out_class_num == 3:
            self._diagnosis = [DIAGNOSIS_MAP[d] for d in diagnosis]
        elif self.out_class_num == 2:
            self._diagnosis = [DIAGNOSIS_MAP_binary[d] for d in diagnosis]

        self._rid = rid

    def __len__(self) -> int:
        return len(self._image_data)

    def __getitem__(self, index: int):
        label = self._diagnosis[index]
        scans = self._image_data[index]

        assert len(scans) == len(self.transforms)

        if self.with_mri is True and self.with_pet is True:
            sample = []
            for scan, transform in zip(scans, self.transforms):
                sample.append(transform(scan))
            sample = tuple(sample)
        elif self.with_mri is True or self.with_pet is True:           
            sample = self.transforms[0](scans)

        return sample, label

