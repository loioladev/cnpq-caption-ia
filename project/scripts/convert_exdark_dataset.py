import os
import shutil
from PIL import Image
import argparse

# 0 - labels
# 1 - light
# 2 - in/out
LABEL_CLASS = 0


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert ExDark dataset to YOLO format")
    parser.add_argument(
        "--src_path",
        type=str,
        required=True,
        help="Path to the ExDark dataset",
    )
    parser.add_argument(
        "--new_path",
        type=str,
        required=True,
        help="Path to the new directory to save the YOLO dataset",
    )
    parser.add_argument(
        "--class_list_path",
        type=str,
        required=True,
        help="Path to the class list file",
    )
    parser.add_argument(
        "--enhance_images",
        type=bool,
        default=False,
        help="Enhance images",
    )
    return parser


def convert_txt_file_name(files: list, new_path: str) -> str:
    if not files[0].endswith(".txt"):
        files = [os.path.basename(file) for file in files]
        files = [os.path.join(new_path, file) for file in files]
        return files

    new_files = []
    for file in files:
        file = os.path.basename(file)
        new_file = file.split(".")[0] + ".txt"
        new_file = os.path.join(new_path, new_file)
        new_files.append(new_file)
    return new_files


def move_files(folders: list, new_path: str) -> None:
    os.makedirs(new_path, exist_ok=True)
    for folder in folders:
        files = os.listdir(folder)
        files = [os.path.join(folder, file) for file in files]
        new_files = convert_txt_file_name(files, new_path)
        [shutil.copy(file, new_file) for file, new_file in zip(files, new_files)]


def create_yolo_directory(src_path: str, new_path: str) -> None:
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    os.makedirs(new_path, exist_ok=True)

    for folder in os.listdir(src_path):
        new_folder_path = os.path.join(new_path, folder)
        folder_path = os.path.join(src_path, folder)
        class_folders = os.listdir(folder_path)
        class_folders = [
            os.path.join(folder_path, class_folder) for class_folder in class_folders
        ]
        move_files(class_folders, new_folder_path)
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
    create_yolo_directory(src_path, new_path)

    images_to_jpg(os.path.join(new_path, "images"))
    if enhance_images:
        image_enhancement(os.path.join(new_path, "images"))

    convert_labels_to_yolo(new_path, class_path)
    divide_dataset(new_path, class_path)


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
