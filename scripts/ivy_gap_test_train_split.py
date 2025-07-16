from pathlib import Path
import shutil
import random

random.seed(10)

ROOT_DIR = Path("../Ivy_gap_dataset")
TEST_DIR = ROOT_DIR / "test"
TESTANNOT_DIR = ROOT_DIR / "testannot"
VAL_DIR = ROOT_DIR / "val"
VALANNOT_DIR = ROOT_DIR / "valannot"
TRAIN_DIR = ROOT_DIR / "train"
TRAINANNOT_DIR = ROOT_DIR / "trainannot"

for directory in [
    TEST_DIR,
    TESTANNOT_DIR,
    VAL_DIR,
    VALANNOT_DIR,
    TRAIN_DIR,
    TRAINANNOT_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

percent_test = 0.05
percent_val = 0.05
percent_train = 0.9

image_names = list((ROOT_DIR / "Annotated" / "Resized").glob("*.png"))
# image_names = [i.name.split('_')[-1] for i in image_names]
# specimen_names = [i.split('_')[0] for i in image_names]
random.shuffle(image_names)

n_test = int(percent_test * len(image_names))
n_val = int(percent_val * len(image_names))
n_train = len(image_names) - n_test - n_val

test_images = image_names[:n_test]
val_images = image_names[n_test : n_test + n_val]
train_images = image_names[n_test + n_val :]


for annot_img in test_images:
    try:
        he_img_name = annot_img.name.split("_")
        he_img_name[1] = "HE"
        he_img_name = "_".join(he_img_name)
        he_img = ROOT_DIR / "H&Es" / "Resized" / he_img_name
        shutil.copy2(he_img, TEST_DIR / he_img.name)
        shutil.copy2(annot_img, TESTANNOT_DIR / annot_img.name)
    except FileNotFoundError:
        print(f"{he_img} not found")

for annot_img in val_images:
    try:
        he_img_name = annot_img.name.split("_")
        he_img_name[1] = "HE"
        he_img_name = "_".join(he_img_name)
        he_img = ROOT_DIR / "H&Es" / "Resized" / he_img_name
        shutil.copy2(he_img, VAL_DIR / he_img.name)
        shutil.copy2(annot_img, VALANNOT_DIR / annot_img.name)
    except FileNotFoundError:
        print(f"{he_img} not found")

for annot_img in train_images:
    try:
        he_img_name = annot_img.name.split("_")
        he_img_name[1] = "HE"
        he_img_name = "_".join(he_img_name)
        he_img = ROOT_DIR / "H&Es" / "Resized" / he_img_name
        shutil.copy2(he_img, TRAIN_DIR / he_img.name)
        shutil.copy2(annot_img, TRAINANNOT_DIR / annot_img.name)
    except FileNotFoundError:
        print(f"{he_img} not found")

n_test_img = len(list(TEST_DIR.glob("*.png")))
n_test_img_annot = len(list(TESTANNOT_DIR.glob("*.png")))
assert n_test_img == n_test_img_annot == n_test

n_train_img = len(list(TRAIN_DIR.glob("*.png")))
n_train_img_annot = len(list(TRAINANNOT_DIR.glob("*.png")))
assert n_train_img == n_train_img_annot == n_train

n_val_img = len(list(VAL_DIR.glob("*.png")))
n_val_img_annot = len(list(VALANNOT_DIR.glob("*.png")))
assert n_val_img == n_val_img_annot == n_val
