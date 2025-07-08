from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


DIR_ANNOTATED = Path("Ivy_gap_dataset/Annotated")
DIR_HE = Path("Ivy_gap_dataset/HE")

DIR_RESIZED_HE = Path(DIR_HE / "Resized")
DIR_RESIZED_HE.mkdir(exist_ok=True)

DIR_RESIZED_ANNOTATED = Path(DIR_ANNOTATED / "Resized_annotated")
DIR_RESIZED_ANNOTATED.mkdir(exist_ok=True)

for file in DIR_ANNOTATED.glob("*.jpg"):
    image = Image.open(file)
    image = image.resize((1024, 1024),resample=Image.NEAREST)
    image.save(DIR_RESIZED_ANNOTATED/file.name)
