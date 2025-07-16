import os
from pathlib import Path
import torch
import torch.utils.data as data
import numpy as np
from PIL import Image
from torchvision.datasets.folder import is_image_file, default_loader

classes = [
    "GBM",
    "Leading Edge Region",
    "Hyperplastic blood vessels",
    "infiltrating tumor region",
    "Cellular tumor region",
    "Perinecrotic zone",
    "Pseudopalisading cells but no visible necrosis",
    "Pseudopalisading cells around necrosis",
    "Microvascular Proliferation",
    "Necrosis",
]

class_color = [
    (0, 114, 201),
    (33, 143, 165),
    (255, 102, 0),
    (209, 4, 208),
    (5, 208, 4),
    (67, 209, 248),
    (5, 4, 208),
    (5, 208, 170),
    (255, 51, 0),
    (6, 5, 5),
]


def label_to_long_tensor(pic):
    if isinstance(pic, np.ndarray):
        # handle numpy array
        label = torch.from_numpy(pic).long()
    else:
        label = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))
        label = label.view(pic.size[1], pic.size[0], 1)
        label = label.transpose(0, 1).transpose(0, 2).squeeze().contiguous().long()
    return label


class IvyGap(data.Dataset):
    def __init__(
        self,
        root,
        split="train",
        joint_transform=None,
        transform=None,
        target_transform=label_to_long_tensor,
        loader=default_loader,
    ):
        self.root = Path(root)
        assert split in ("train", "val", "test")
        self.split = split
        self.joint_transform = joint_transform
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader
        self.imgs = list((self.root / self.split).glob("*.jpg"))

    def __getitem__(self, index):
        path = str(self.imgs[index])
        img = self.loader(path)
        target_path = path.replace(self.split, self.split + "annot")
        target_path = target_path.replace("HE", "TFA")
        target = self.loader(target_path)  # Image.open ?

        if self.joint_transform is not None:
            img, target = self.joint_transform([img, target])

        if self.transform is not None:
            img = self.transform(img)

        target = self.target_transform(target)
        return img, target

    def __len__(self):
        return len(self.imgs)
