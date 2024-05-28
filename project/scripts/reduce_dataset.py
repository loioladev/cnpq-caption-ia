import os
import shutil
from collections import defaultdict
import json

def read_label(label_path: str) -> dict:
    with open(label_path, 'r') as f:
        instances = f.readlines()
    
    instances = [int(instance.split(' ')[0]) for instance in instances]
  
    label_info = defaultdict(int)
    for instance in instances:
        label_info[instance] += 1

    return label_info


def get_labels_from_json(json_path: str) -> dict:
    with open(json_path, 'r') as f:
        return json.load(f)
    
    
def get_labels_from_dir(dir_path: str, json_path: str = '') -> dict:
    labels = dict()
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        labels[file_path] = read_label(file_path)
    
    if not json_path:
        return labels

    with open(json_path, 'w') as f:
        json.dump(labels, f)
    
    return labels

def count_labels(labels: dict) -> dict:
    count = defaultdict(int)
    for _, values in labels.items():
        for label, value in values.items():
            count[label] += value
    
    return count


def show_difference(count_original: dict, count_reduced: dict):
    labels = count_original.keys()
    labels = [int(label) for label in labels]
    labels = sorted(labels)
    labels = [str(label) for label in labels]
    for label in labels:
        print(f"Label {label}: {count_original[label]} -> {count_reduced[int(label)]}")

def iterate_labels(labels_og: dict, files_per_class: dict, labels_count: list, new_dir) -> list:
    min_label_idx = -1
    last_seen = 10000000
    for i in range(len(labels_count)):
        if labels_count[i][0] < last_seen:
            last_seen = labels_count[i][0]
            min_label_idx = i


    class_found = labels_count[min_label_idx][1]
    if not files_per_class[class_found]:
        labels_count[min_label_idx] = (10000000, class_found)
        return labels_count, None

    file_name, _ = files_per_class[class_found].pop()

    dst_path = os.path.join(new_dir, os.path.basename(file_name))
    if os.path.exists(dst_path):
        return labels_count, file_name
    
    shutil.copy(file_name, dst_path)
    for label, value in labels_og[file_name].items():
        for i in range(len(labels_count)):
            if labels_count[i][1] == label:
                labels_count[i] = (labels_count[i][0] + value, label)
                break

    return labels_count, file_name

def reduce_labels(labels: dict, reduce_to: int, new_dir: str) -> dict:
    
    files_per_class = defaultdict(list)
    for file_name, labels_info in labels.items():
        for label, value in labels_info.items():
            files_per_class[label].append((file_name, value))
    
    for label, files in files_per_class.items():
        files_per_class[label] = sorted(files, key=lambda x: x[1])

    labels_count = count_labels(labels)
    labels_count = [(0, label)  for label, value in labels_count.items()]

    seen = set()
    total = 0
    while total < reduce_to:
        labels_count, file_nm = iterate_labels(labels, files_per_class, labels_count, new_dir)
        if not file_nm:
            continue
        if file_nm in seen:
            continue
        seen.add(file_nm)
        total += 1



def main():
    # args
    label_dir = '/media/matheus/Game/College/cnpq_caption/datasets/lvis/labels/val2017'
    new_dir = './val2017_reduced'
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.makedirs(new_dir, exist_ok=True)
    json_path = os.path.join(os.getcwd(),f'labels_{os.path.basename(label_dir)}.json')
    reduce_to = 0.25 * len(os.listdir(label_dir))

    # get labels of each file
    if os.path.exists(json_path):
        labels = get_labels_from_json(json_path)
    else:
        labels = get_labels_from_dir(label_dir, json_path)


    reduce_labels(labels, reduce_to, new_dir)

    count_original = count_labels(labels)
    count_reduced = {}
    for file in os.listdir(new_dir):
        file_path = os.path.join(new_dir, file)
        count_reduced[file_path] = read_label(file_path)
    count_reduced = count_labels(count_reduced)

    show_difference(count_original, count_reduced)

    print("Done!")


if __name__ == '__main__':
    main()