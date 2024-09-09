"""
TODO: Add description
"""

import argparse
import os
import shutil
import sys

import cv2
import tqdm
from PIL import Image

# 0 - labels
# 1 - light
# 2 - in/out
LABEL_CLASS = 0
# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
IMAGE_TYPE = "jpeg"


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for the script.
    :return: A instance of the argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Convert ExDark dataset to YOLO format"
    )
    parser.add_argument(
        "src_path",
        type=str,
        help="Path to the ExDark dataset",
    )
    parser.add_argument(
        "yolo_path",
        type=str,
        help="Path to the new directory to save the YOLO dataset",
    )
    parser.add_argument(
        "class_list_path",
        type=str,
        help="Path to the class list file",
    )
    return parser


def convert_txt_file_name(folder_path: str) -> str:
    """
    Remove aditional information from the label file names.
    :param folder_path: Path to the folder containing the label files.
    :return: List of new label files.
    """
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    if not files or not files[0].endswith(".txt"):
        return

    for file in files:
        new_file = os.path.basename(file).split(".")[0] + ".txt"
        new_file = os.path.join(folder_path, new_file)
        shutil.move(file, new_file)


def create_yolo_directory(src_path: str, yolo_path: str) -> None:
    """
    Create YOLO directory structure and copy files.
    :param src_path: Path to the ExDark dataset.
    :param yolo_path: Path to the new directory to save the YOLO dataset.
    """
    if os.path.exists(yolo_path):
        user_decision = input(f"Path {yolo_path} exists. Delete it? (y/n): ")
        shutil.rmtree(yolo_path) if user_decision.lower() == "y" else sys.exit()

    os.makedirs(yolo_path)
    for type_folder in os.listdir(src_path):
        # Get labels and images folders
        type_folder_path = os.path.join(src_path, type_folder)
        new_type_folder_path = os.path.join(yolo_path, type_folder)

        # Get classes folders and copy files
        classes_folder = os.listdir(type_folder_path)
        classes_folder = [
            os.path.join(type_folder_path, folder) for folder in classes_folder
        ]
        for class_folder in classes_folder:
            shutil.copytree(class_folder, new_type_folder_path, dirs_exist_ok=True)

        # Modify label files names
        convert_txt_file_name(new_type_folder_path)
    print("Directory created successfully")


def convert_label(file_path: str, class_id: str, image_size: tuple) -> None:
    """
    Convert label file from ExDark format to YOLO format, in xywhn.
    :param file_path: Path to the label file.
    :param class_id: Class id of the label.
    :param image_size: Size of the image in format (width, height).
    """
    # Open file and remove first line (unused)
    with open(file_path, "r") as f:
        lines = f.readlines()
    lines = lines[1:]

    image_width = image_size[0]
    image_height = image_size[1]
    new_lines = []
    for line in lines:
        line = line.split(" ")[1:]

        # Calculate xywhn
        x, y, w, h = map(float, line[:4])
        x_center = (x + (w // 2)) / image_width
        y_center = (y + (h // 2)) / image_height
        width = w / image_width
        height = h / image_height

        # Add new line to list
        new_line = f"{class_id} {x_center} {y_center} {width} {height}"
        new_lines.append(new_line)

    # Overwrite file with new labels
    with open(file_path, "w") as f:
        f.write("\n".join(new_lines))


def get_class_dict(class_path: str) -> dict:
    """
    Get class dictionary from image class list file, which contains the
    class id, ambient light, ambient location and split.
    :param class_path: Path to the class list file.
    :return: Dictionary containing the class information.
    """
    # Read image class list file
    with open(class_path, "r") as f:
        class_files = f.readlines()
    class_files = class_files[1:]

    # Convert image class list to dictionary
    class_dict = {}
    for class_file in class_files:
        class_file = class_file.split(" ")
        file_name = class_file[0].split(".")[0]
        class_dict[file_name] = class_file[1:]
    return class_dict


def convert_labels_to_yolo(yolo_path: str, class_path: str) -> None:
    """
    Convert folder of labels from ExDark format to YOLO format.
    :param yolo_path: Path to the yolo directory.
    :param class_path: Path to the class list file.
    """
    class_dict = get_class_dict(class_path)

    # Get image files path
    images_path = os.path.join(yolo_path, "images")
    image_files = [
        os.path.join(images_path, image) for image in os.listdir(images_path)
    ]

    # Get label files path
    labels_path = os.path.join(yolo_path, "labels")
    label_files = [
        os.path.join(labels_path, label) for label in os.listdir(labels_path)
    ]
    image_files = sorted(image_files)
    label_files = sorted(label_files)

    # Convert labels
    for image_file, label_file in zip(image_files, label_files):
        image_size = Image.open(image_file).size
        file_name = os.path.basename(label_file).split(".")[0]
        class_id = int(class_dict[file_name][LABEL_CLASS]) - 1
        convert_label(label_file, class_id, image_size)
    print("Labels converted successfully")


def image_enhancement(images_path: str) -> None:
    """
    Use CLAHE algorithm in images.
    :param images_path: Path to the image directory.
    """

    for image in tqdm(os.listdir(images_path), desc="Applying CLAHE in images"):
        image_path = os.path.join(images_path, image)
        image = cv2.imread(image_path)

        # Convert image to LAB and use CLAHE
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab_planes = cv2.split(lab)
        lab_planes_list = list(lab_planes)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab_planes_list[0] = clahe.apply(lab_planes_list[0])
        lab = cv2.merge(lab_planes_list)
        image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        cv2.imwrite(image_path, image)
    print("Images enhanced with CLAHE succesfully")


def divide_dataset(yolo_path: str, class_path: str) -> None:
    """
    Divide dataset in train, validation and test sets.
    :param yolo_path: Path to the yolo directory.
    :param class_path: Path to the class list file.
    """
    class_dict = get_class_dict(class_path)
    images_path = os.path.join(yolo_path, "images")
    labels_path = os.path.join(yolo_path, "labels")

    new_folder_image = os.path.join(yolo_path, "images_subset")
    new_folder_label = os.path.join(yolo_path, "labels_subset")
    directories = ["train", "val", "test"]
    for directory in directories:
        os.makedirs(os.path.join(new_folder_image, directory), exist_ok=True)
        os.makedirs(os.path.join(new_folder_label, directory), exist_ok=True)

    for file_name, value in class_dict.items():
        # Get images and labels
        image_file = os.path.join(images_path, file_name + "." + IMAGE_TYPE)
        label_file = os.path.join(labels_path, file_name + ".txt")
        split_dir = directories[int(value[3]) - 1]

        # Copy images and labels
        shutil.copy(
            image_file,
            os.path.join(new_folder_image, split_dir, file_name + "." + IMAGE_TYPE),
        )
        shutil.copy(
            label_file, os.path.join(new_folder_label, split_dir, file_name + ".txt")
        )

    shutil.rmtree(images_path)
    shutil.rmtree(labels_path)
    shutil.move(new_folder_image, images_path)
    shutil.move(new_folder_label, labels_path)
    print("Dataset divided successfully")


def convert_images_to_format(yolo_path: str, image_type: str) -> None:
    """
    Convert images to a specific format.
    :param yolo_path: Path to the yolo directory.
    :param image_type: Image format to convert.
    """
    images_path = os.path.join(yolo_path, "images")
    image_files = [
        os.path.join(images_path, image) for image in os.listdir(images_path)
    ]

    progress_bar = tqdm.tqdm(image_files, desc="Converting images", unit="image")
    for image_file in progress_bar:
        if image_file.endswith(image_type):
            continue
        image = Image.open(image_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
        new_image_file = image_file.split(".")[0] + "." + image_type
        image.save(new_image_file, format=image_type.upper())
        os.remove(image_file)
    print("Images converted successfully")


def convert_dataset_to_yolo(src_path: str, yolo_path: str, class_path: str) -> None:
    """
    Convert ExDark dataset to YOLO format.
    :param src_path: Path to the ExDark dataset.
    :param yolo_path: Path to the new directory to save the YOLO dataset.
    :param class_path: Path to the class list file.
    """
    create_yolo_directory(src_path, yolo_path)
    convert_images_to_format(yolo_path, IMAGE_TYPE)
    convert_labels_to_yolo(yolo_path, class_path)
    image_enhancement(os.path.join(yolo_path, "images"))
    divide_dataset(yolo_path, class_path)


def main():
    parser = create_parser()
    args = parser.parse_args()
    src_path = args.src_path
    yolo_path = args.yolo_path
    class_list_path = args.class_list_path
    convert_dataset_to_yolo(src_path, yolo_path, class_list_path)


if __name__ == "__main__":
    main()
