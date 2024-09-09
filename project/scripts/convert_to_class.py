import argparse
import os
import shutil

label_type = "light"

light_class = {
    "1": "Low",
    "2": "Ambient",
    "3": "Object",
    "4": "Single",
    "5": "Weak",
    "6": "Strong",
    "7": "Screen",
    "8": "Window",
    "9": "Shadow",
    "10": "Twilight",
}

in_out_class = {"1": "Indoor", "2": "Outdoor"}

train_val_test_dict = {"1": "train", "2": "val", "3": "test"}


def create_parser() -> argparse.ArgumentParser:
    """Create a parser for the command line arguments"""
    parser = argparse.ArgumentParser(
        description="Convert labels to YOLO classification task."
    )
    parser.add_argument("path_to_images", type=str, help="Path to images directory")
    parser.add_argument(
        "path_to_labels", type=str, help="Path to text file with labels"
    )
    parser.add_argument("label_path", type=str, help="Path to save the labels")
    return parser


def convert_to_class(path_to_images: str, path_to_labels: str, label_path: str) -> None:
    """
    Convert the labels to a YOLO classification task

    :param path_to_images: The path to the images
    :param path_to_labels: The path to the labels
    :param label_path: The path to save the labels
    """
    with open(path_to_labels, "r") as file:
        labels = file.readlines()

    # Name | Class | Light | In/Out | Train/Val/Test
    for line in labels:
        image_name, class_, light, in_out, train_val_test = line.split(" ")
        image_name = image_name.split(".")[0] + ".jpg"

        if label_type == "light":
            classification = light_class[light]
        else:
            classification = in_out_class[in_out]

        train_val_test = train_val_test.split()[0]
        data_train_type = train_val_test_dict[train_val_test]

        class_path = os.path.join(label_path, data_train_type, classification)
        os.makedirs(class_path, exist_ok=True)

        image_path = os.path.join(path_to_images, image_name)
        shutil.copy(image_path, os.path.join(class_path, image_name))


def main():
    args = create_parser().parse_args()
    convert_to_class(args.path_to_images, args.path_to_labels, args.label_path)


if __name__ == "__main__":
    main()
