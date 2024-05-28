import json
import os
import shutil
from collections import defaultdict
import argparse
import matplotlib.pyplot as plt

def parse_args() -> argparse.Namespace:
    """
    Create parser for command line arguments.
    :return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Create a subset of the original dataset.')
    parser.add_argument('label_dir', type=str, help='The path to the directory containing the labels.')
    parser.add_argument('output_dir', type=str, help='The path to the directory where the subset will be saved.')
    parser.add_argument('percentage', type=int, help='The percentage of the original dataset that will be used [5-99]%.')
    return parser.parse_args()

def verify_args(args: argparse.Namespace) -> None:
    """
    Verify if the arguments are valid.
    :param args: The parsed arguments.
    """
    if not os.path.isdir(args.label_dir):
        raise FileNotFoundError(f"Directory '{args.label_dir}' not found.")
    if not 5 <= args.percentage <= 99:
        raise ValueError("The percentage must be between 5 and 99.")
    if os.path.exists(args.output_dir):
        raise FileExistsError(f"Directory '{args.output_dir}' already exists.")
    os.makedirs(args.output_dir)
    

def read_label_file(file_path: str) -> dict:
    """
    Read the labels of the given file.
    :param file_path: The path to the file containing the labels.
    :return: A dictionary containing the labels of the file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    labels = [int(line.split(' ')[0]) for line in lines]
  
    label_counts = defaultdict(int)
    for label in labels:
        label_counts[label] += 1

    return label_counts


def get_labels_from_directory(directory_path: str) -> dict:
    """
    Read the labels of each file in the given directory.
    :param directory_path: The path to the directory containing the labels.
    :return: A dictionary containing the labels of each file.
    """
    labels = dict()
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        labels[file_path] = read_label_file(file_path)
    return labels

def get_dataset_labels(label_dir: str, label_json_path: str) -> dict:
    """
    Get the labels of each file in the dataset.
    :param label_dir: The path to the directory containing the labels.
    :param label_json: The path to the JSON file containing the labels.
    :return: A dictionary containing the labels of each file.
    """
    if os.path.exists(label_json_path):
        with open(label_json_path, 'r') as file:
            labels = json.load(file)
    else:
        labels = get_labels_from_directory(label_dir)
        print(f"Saving labels to '{label_json_path}'...")
        with open(label_json_path, 'w') as file:
            json.dump(labels, file)
    return labels


def iterate_labels(label_data: dict, files_grouped_by_label: dict, label_order: list, output_dir: str) -> tuple:
    """
    Iterate over labels to find the file to add to the subset and update label counts.
    :param label_data: A dictionary containing the labels of each file.
    :param files_grouped_by_label: A dictionary containing the files grouped by label.
    :param label_order: A list containing the number of instances of each class.
    :param output_dir: The path to the directory where the subset will be saved.
    :return: A tuple containing the updated label order and the selected file path.
    """
    # Find the class with the lowest number of instances
    min_label_idx = 0
    lowest_count = float('inf')
    for i, (count, label) in enumerate(label_order):
        if count < lowest_count:
            lowest_count = count
            min_label_idx = i

    # Select the file with the lowest number of instances
    selected_label = label_order[min_label_idx][1]
    if not files_grouped_by_label[selected_label]:
        label_order[min_label_idx] = (float('inf'), selected_label)
        return label_order, None
    selected_file, _ = files_grouped_by_label[selected_label].pop()

    # Copy the file to the output directory if it does not exist
    dst_path = os.path.join(output_dir, os.path.basename(selected_file))
    if os.path.exists(dst_path):
        return label_order, None
    shutil.copy(selected_file, dst_path)

    # Update the number of instances of the selected class
    for label, count in label_data[selected_file].items():
        for i, (current_count, current_label) in enumerate(label_order):
            if current_label != label:
                continue
            label_order[i] = (current_count + count, current_label)
            break

    return label_order, selected_file


def create_subset(label_data: dict, output_dir: str, subset_size: int) -> None:
    """
    Create a subset of the dataset.
    :param label_data: A dictionary containing the labels of each file.
    :param output_dir: The path to the directory where the subset will be saved.
    :param subset_size: The number of files in the subset.
    """

    # Insert the files in a dictionary grouped by label
    files_grouped_by_label = defaultdict(list)
    for file_name, label_info in label_data.items():
        for label, count in label_info.items():
            files_grouped_by_label[label].append((file_name, count))
    
    # Sort the files inside classes by the number of labels in descending order
    for label, files in files_grouped_by_label.items():
        files_grouped_by_label[label] = sorted(files, key=lambda x: x[1], reverse=True)

    # Create a list to store the number of instances of each class which were already selected
    label_order = [(0, label) for label in files_grouped_by_label.keys()]

    # Create subset of the dataset in the output directory
    total_selected = 0
    while total_selected < subset_size:
        label_order, selected_file = iterate_labels(label_data, files_grouped_by_label, label_order, output_dir)
        if not selected_file:
            continue
        total_selected += 1
    

def count_labels(label_data: dict) -> dict:
    """
    Count the number of instances of each class in the dataset.
    :param label_data: A dictionary containing the labels of each file.
    :return: A dictionary containing the number of instances of each class.
    """
    count = defaultdict(int)
    for _, values in label_data.items():
        for label, value in values.items():
            count[label] += value
    return count


def plot_data(count_original: dict, count_subset: dict) -> None:
    """
    Plot the number of instances of each class in the original and subset datasets.
    :param count_original: A dictionary containing the number of instances of each class in the original dataset.
    :param count_subset: A dictionary containing the number of instances of each class in the subset dataset.
    """
    classes = list(count_original.keys())
    values_original = list(count_original.values())
    values_subset = list(count_subset.values())

    bar_width = 0.35
    fig, ax = plt.subplots()

    ax.bar(classes, values_original, bar_width, label='Original')
    ax.bar(classes, values_subset, bar_width, label='Subset')
    
    ax.set_xlabel('Classes')
    ax.set_ylabel('Number of instances')
    ax.set_title('Number of instances per class')
    ax.legend()

    ax.xaxis.set_ticks([])
    ax.set_ylim(0, max(values_subset) + 1)

    plt.savefig(os.path.join(os.getcwd(), 'subset_distribution.png'))


def main():
    args = parse_args()
    verify_args(args)

    label_dir = args.label_dir
    label_json = os.path.join(os.getcwd(), f'label_{os.path.basename(label_dir)}.json')
    output_dir = args.output_dir
    subset_size = (args.percentage / 100) * len(os.listdir(label_dir))
  
    labels = get_dataset_labels(label_dir, label_json)
    create_subset(labels, output_dir, subset_size)

    count_original = count_labels(labels)
    count_subset = count_labels(get_labels_from_directory(output_dir))
    plot_data(count_original, count_subset)

    print("Done!")


if __name__ == '__main__':
    main()