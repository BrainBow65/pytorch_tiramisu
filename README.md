# One Hundred Layers Tiramisu

The goal of this project is to segment whole-slide images from glioblastomta ([Shirazi et al., 2021](https://www.nature.com/articles/s41416-021-01394-x)) using a fully convolutional DenseNet ([Jegou el al., 2017](https://arxiv.org/pdf/1611.09326)).

## Data Preparation

- Run `/scripts/data_retrieval_ivygap.py` to download the whole slide images from the [Ivy GAP dataset](https://glioblastoma.alleninstitute.org/). The images will be stored in a directory `Ivy_gap_dataset` at the root of this repo. The stained images are stored in the subdirectory `H&E` and the annotated images in the subdirectory `Annotated`

- Run `/scripts/resize_ivy_gap.py` to resize the images to 1024x1024 and, for the annotated images, discretize their colors to the values stores in `colors.csv`. The resulting images are stored in the `Resized` directory within the `H&E` and `Annotated` directories

- Run `scripts/ivy_gap_test_train_split.py` to divide the data into train, validation and test set. For each set, there are separate directories for stained and annotated images (e.g. `train`, `trainannot`) within the `Ivy_gap_dataset` directory
