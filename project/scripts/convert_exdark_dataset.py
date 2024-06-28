import os
import shutil
from PIL import Image
import argparse
import sys

# 0 - labels
# 1 - light
# 2 - in/out
LABEL_CLASS = 0


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for the script.
    :return: A instance of the argument parser.
    """
    parser = argparse.ArgumentParser(description="Convert ExDark dataset to YOLO format")
    parser.add_argument(
        "src_path",
        type=str,
        help="Path to the ExDark dataset",
    )
    parser.add_argument(
        "new_path",
        type=str,
        help="Path to the new directory to save the YOLO dataset",
    )
    parser.add_argument(
        "class_list_path",
        type=str,
        help="Path to the class list file",
    )
    parser.add_argument(
        "--enhance_images",
        type=bool,
        default=False,
        help="Whether to enhance images to improve brightness and contrast",
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


def create_yolo_directory(src_path: str, new_path: str) -> None:
    """
    Create YOLO directory structure and copy files.
    :param src_path: Path to the ExDark dataset.
    :param new_path: Path to the new directory to save the YOLO dataset.
    """
    if os.path.exists(new_path):
        user_decision = input(f"Path {new_path} exists. Delete it? (y/n): ")
        shutil.rmtree(new_path) if user_decision.lower() == "y" else sys.exit()

    os.makedirs(new_path)
    for type_folder in os.listdir(src_path):
        # Get labels and images folders
        type_folder_path = os.path.join(src_path, type_folder)
        new_type_folder_path = os.path.join(new_path, type_folder)

        # Get classes folders and copy files
        classes_folder = os.listdir(type_folder_path)
        classes_folder = [os.path.join(type_folder_path, folder) for folder in classes_folder]
        [shutil.copytree(class_folder, new_type_folder_path, dirs_exist_ok=True) for class_folder in classes_folder]

        # Modify label files names
        convert_txt_file_name(new_type_folder_path)
    print("Directory created successfully")


def convert_label(file_path: str, class_id: str, image_size: tuple) -> None:
    with open(file_path, "r") as f:
        lines = f.readlines()
    lines = lines[1:]

    new_lines = []
    for line in lines:
        line = line.split(" ")
        # Calculate xywh
        x, y, w, h = int(line[1]), int(line[2]), int(line[3]), int(line[4])
        x_center = x + (w // 2)
        y_center = y + (h // 2)
        width = w
        height = h

        # Normalize
        x_center /= image_size[0]
        y_center /= image_size[1]
        width /= image_size[0]
        height /= image_size[1]

        new_line = f"{class_id} {x_center} {y_center} {width} {height}"
        new_lines.append(new_line)

    with open(file_path, "w") as f:
        f.write("\n".join(new_lines))


def get_class_dict(class_path: str) -> dict:
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


def convert_labels_to_yolo(new_path: str, class_path: str) -> None:
    class_dict = get_class_dict(class_path)

    # Convert labels to yolo format
    images_path = os.path.join(new_path, "images")
    image_files = [
        os.path.join(images_path, image) for image in os.listdir(images_path)
    ]
    labels_path = os.path.join(new_path, "labels")
    label_files = [
        os.path.join(labels_path, label) for label in os.listdir(labels_path)
    ]
    for image_file, label_file in zip(image_files, label_files):
        image = Image.open(image_file)
        width, height = image.size

        file_name = os.path.basename(label_file).split(".")[0]
        class_id = class_dict[file_name][LABEL_CLASS]

        convert_label(label_file, class_id, (width, height))

    print("Labels converted successfully")


def images_to_jpg(dir_path: str) -> None:
    for image in os.listdir(dir_path):
        if image.endswith(".jpg"):
            continue
        image_path = os.path.join(dir_path, image)
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        new_image_path = image_path.split(".")[0] + ".jpg"
        img.save(new_image_path)
        os.remove(image_path)
    print("Images converted successfully")


def image_enhancement(dir_path: str) -> None:
    pass


def divide_dataset(new_path: str, class_path: str) -> None:
    class_dict = get_class_dict(class_path)
    images_path = os.path.join(new_path, "images")
    labels_path = os.path.join(new_path, "labels")

    new_folder_image = os.path.join(new_path, "images_subset")
    new_folder_label = os.path.join(new_path, "labels_subset")
    directories = ["train", "val", "test"]
    for directory in directories:
        os.makedirs(os.path.join(new_folder_image, directory), exist_ok=True)
        os.makedirs(os.path.join(new_folder_label, directory), exist_ok=True)

    for key, value in class_dict.items():
        # Get images and labels
        image_file = os.path.join(images_path, key + ".jpg")
        label_file = os.path.join(labels_path, key + ".txt")
        dest_dir = directories[int(value[3]) - 1]

        # Copy images and labels
        shutil.copy(image_file, os.path.join(new_folder_image, dest_dir, key + ".jpg"))
        shutil.copy(label_file, os.path.join(new_folder_label, dest_dir, key + ".txt"))

    print("Dataset divided successfully")


def convert_dataset_to_yolo(src_path: str, new_path: str, class_path: str, enhance_images: bool) -> None:
    """
    Convert ExDark dataset to YOLO format.
    :param src_path: Path to the ExDark dataset.
    :param new_path: Path to the new directory to save the YOLO dataset.
    :param class_path: Path to the class list file.
    :param enhance_images: Whether to enhance images or not.
    """
    create_yolo_directory(src_path, new_path)

    # images_to_jpg(os.path.join(new_path, "images"))
    # if enhance_images:
    #     image_enhancement(os.path.join(new_path, "images"))

    # convert_labels_to_yolo(new_path, class_path)
    # divide_dataset(new_path, class_path)


def main():
    parser = create_parser()
    args = parser.parse_args()

    src_path = args.src_path
    new_path = args.new_path
    class_list_path = args.class_list_path
    enhance_images = args.enhance_images
    convert_dataset_to_yolo(src_path, new_path, class_list_path, enhance_images)


if __name__ == "__main__":
    main()
