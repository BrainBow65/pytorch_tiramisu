from pathlib import Path
import shutil
import random
random.seed(10)

ROOT_DIR = Path("Ivy_gap_dataset")
TEST_DIR = ROOT_DIR/"test"
TESTANNOT_DIR = ROOT_DIR/"testannot"

percent_test = 0.05
percent_val = 0.05
percent_train = 0.9

image_names = list((ROOT_DIR/"Annotated"/"Resized").glob("*.jpg"))
# image_names = [i.name.split('_')[-1] for i in image_names]
# specimen_names = [i.split('_')[0] for i in image_names]
random.shuffle(image_names)

n_test = int(percent_test * len(image_names))
n_val = int(percent_val * len(image_names))
n_train = len(image_names) - n_test - n_val

test_images = image_names[:n_test]
val_images = image_names[n_test:n_test + n_val]
train_images = image_names[n_test + n_val:]


for annot_img in test_images:
    try:
        he_img_name = annot_img.name.split('_')
        he_img_name[1]='HE'
        he_img_name = '_'.join(he_img_name)
        he_img = ROOT_DIR/"H&Es"/"Resized"/he_img_name
        shutil.copy2(he_img, TEST_DIR / he_img.name)
        shutil.copy2(annot_img, TESTANNOT_DIR / annot_img.name)
    except FileNotFoundError:
        print(f"{he_img} not found")
