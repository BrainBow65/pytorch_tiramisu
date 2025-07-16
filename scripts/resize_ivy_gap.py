from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
SIZE = (1024, 1024)

# Get RGB values for the different colors in the annotation
rgb_values = np.loadtxt("colors.csv", delimiter=",", dtype=str)
rgb_values = rgb_values[:, :3].astype(int)
n_colors = len(rgb_values)
# Make a color palette
palette = list(rgb_values.flatten())
palette += [255, 255, 255]  # add white
palette += [0, 0, 0] * (256 - n_colors - 1)  # pad to 256 colors
palette_img = Image.new("P", (1, 1))
palette_img.putpalette(palette)

DIR_ANNOTATED = Path("../Ivy_gap_dataset/Annotated")
DIR_HE = Path("../Ivy_gap_dataset/H&Es")

DIR_RESIZED_HE = Path(DIR_HE / "Resized")
DIR_RESIZED_HE.mkdir(exist_ok=True)

DIR_RESIZED_ANNOTATED = Path(DIR_ANNOTATED / "Resized")
DIR_RESIZED_ANNOTATED.mkdir(exist_ok=True)

for f_annotated, f_he in zip(DIR_ANNOTATED.glob("*.jpg"), DIR_HE.glob("*.jpg")):
    image_annotated = Image.open(f_annotated)
    image_annotated = image_annotated.resize(SIZE, resample=Image.NEAREST)
    image_annotated = image_annotated.quantize(palette=palette_img)
    image_annotated.save(
        DIR_RESIZED_ANNOTATED / f_annotated.name.replace(".jpg", ".png")
    )

    image_he = Image.open(f_he)
    image_he = image_he.resize(SIZE, resample=Image.NEAREST)
    image_he.save(DIR_RESIZED_HE / f_he.name.replace(".jpg", ".png"))
