import os


def main():
    src_path = '/media/matheus/Game/College/cnpq_caption/datasets/lvis/labels'
    dst_path = '/media/matheus/Game/College/cnpq_caption/datasets/lvis/detection_labels'

    for directory in os.listdir(src_path):
        if not os.isdir(os.path.join(src_path, directory)):
            continue
        os.makedirs(os.path.join(dst_path, directory), exist_ok=True)
        for filename in os.listdir(os.path.join(src_path, directory)):
            with open(os.path.join(src_path, directory, filename), 'r') as label_file:
                lines = label_file.readlines()
            points = []
            for line in lines:
                split = line.split()
                class_id = split[0]
                for i in range(1, len(split), 2):
                    points.append((split[i], split[i + 1]))


if __name__ == '__main__':
    main()
