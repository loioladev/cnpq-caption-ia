"""
Convert the ExDark dataset to YOLO format.

This script converts the ExDark dataset to YOLO format. The ExDark dataset
is a dataset of images with bounding boxes for the objects in the images.
The YOLO format is a format that contains the class label and the bounding
box coordinates for each object in the image.

Example:
    python convert_exdark.py <src_path> <new_path>
"""

import argparse
import os
import shutil


def create_parser() -> argparse.Namespace:
    """
    Create a parser for the command line arguments.

    :return parser: The parser object.
    """
    parser = argparse.ArgumentParser(
        description="Generate a new dataset with similar words."
    )
    parser.add_argument("src_path", type=str, help="The source path")
    parser.add_argument("new_path", type=str, help="The new path")
    return parser


def move_files(folders: list, new_path: str) -> None:
    """
    Move files from a list of folders to a new path

    :param folders: The list of folders
    :param new_path: The new path
    """
    os.makedirs(new_path, exist_ok=True)
    for folder in folders:
        files = os.listdir(folder)
        files = [os.path.join(folder, file) for file in files]
        [shutil.copy(file, new_path) for file in files]
    return


def create_yolo_directory(src_path: str, new_path: str) -> None:
    """
    Create a YOLO directory from a source path

    :param src_path: The source path
    :param new_path: The new path
    """
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
    return


def main():
    args = create_parser().parse_args()
    create_yolo_directory(args.src_path, args.new_path)


if __name__ == "__main__":
    main()
