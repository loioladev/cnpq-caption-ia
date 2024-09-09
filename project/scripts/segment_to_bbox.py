"""
Segmentation Label to Bounding Box Conversion.

This script is used to convert segmentation labels to bounding box labels.
The script reads the segmentation labels from the input file, converts the
polygon coordinates to bounding box coordinates, and writes the bounding box
labels to the output file in the folder labels_bbox.

The labels of the dataset must be normalized before calling the script.

The directory must be in this formart:
    dataset_dir
    ├── images
    │   ├── train2020
    │   ├── val2021
    │   └── ...
    └── labels
        ├── train2020
        ├── val2021
        └── ...

Example:
    python segment_to_bbox.py <dataset_dir>
"""

import argparse
import os

import cv2

INDEX_OFFSET = 20


def parse_args() -> argparse.Namespace:
    """
    Parse the command-line arguments.

    :return parser: The parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Segmentation Label to Bounding Box Conversion"
    )
    parser.add_argument("dataset_dir", type=str, help="Path to the dataset directory")
    return parser.parse_args()


def read_labels(label_path: str) -> tuple:
    """
    Read the labels from the input file and return the label ids and
    polygon coordinates.

    :param label_path: Path to the input file
    :return: Tuple containing the label ids and polygon coordinates
    """
    with open(label_path, "r") as file:
        lines = file.readlines()

    label_ids = []
    polygon_coordinates = []
    for line in lines:
        parts = line.split()

        label_id = parts[0]
        label_ids.append(int(label_id) + INDEX_OFFSET)

        polygon = list(map(float, parts[1:]))
        polygon_coordinates.append(polygon)

    return label_ids, polygon_coordinates


def polygons_to_bounding_boxes(polygons: list) -> list:
    """
    Convert the polygon coordinates to bounding box coordinates.

    :param polygons: List of polygon coordinates
    :return: List of bounding box coordinates
    """
    normalized_bounding_boxes = []

    for polygon in polygons:
        x_coords = polygon[::2]
        y_coords = polygon[1::2]

        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)

        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        normalized_bbox = [x_center, y_center, width, height]
        normalized_bounding_boxes.append(normalized_bbox)

    return normalized_bounding_boxes


def write_labels(output_path: str, labels: list, xywhn: list) -> None:
    """
    Write labels to the output file in the format:
    <label> <x_center> <y_center> <width> <height>
    for each bounding box in the list.

    :param output_path: Path to the output file
    :param labels: List of labels
    :param xywhn: List of normalized bounding boxes
    :return: None
    """
    lines = []
    for label, bbox in zip(labels, xywhn):
        formatted_bbox = [f"{value:.17f}".rstrip("0").rstrip(".") for value in bbox]
        bbox_str = " ".join(formatted_bbox)
        lines.append(f"{label} {bbox_str}")

    with open(output_path, "w") as output_file:
        output_file.write("\n".join(lines))


def parse_files(label_dir: str, output_dir: str) -> None:
    """
    For each label folder inside directory, read the labels
    and write the bounding box to the output folder.

    :param label_dir: Path to the label folder directory
    :param output_dir: Path to the output folder directory
    :return: None
    """
    for label_file in os.listdir(label_dir):
        label_path = os.path.join(label_dir, label_file)
        output_path = os.path.join(output_dir, label_file)

        labels, polygons = read_labels(label_path)
        xywhn = polygons_to_bounding_boxes(polygons)
        write_labels(output_path, labels, xywhn)


def parse_dataset_labels(dataset_dir: str) -> None:
    """
    Read directory folders to get the images and labels directories and
    parse the folders to verify each directory.

    :param dataset_dir: Path to the dataset directory
    """
    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"Directory '{dataset_dir}' not found")

    labels_dir = os.path.join(dataset_dir, "labels")
    output_dir = os.path.join(dataset_dir, "labels_bbox")
    os.makedirs(output_dir, exist_ok=True)

    for directory in os.listdir(labels_dir):
        label_dir = os.path.join(labels_dir, directory)
        label_output_dir = os.path.join(output_dir, directory)
        os.makedirs(label_output_dir, exist_ok=True)
        parse_files(label_dir, label_output_dir)


def main():
    args = parse_args()
    dataset_dir = args.dataset_dir
    parse_dataset_labels(dataset_dir)


if __name__ == "__main__":
    main()
