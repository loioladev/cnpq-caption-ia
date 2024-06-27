import os
import shutil
import cv2

# 0 - labels
# 1 - light
# 2 - in/out
LABEL_CLASS = 0


def convert_txt_file_name(files: list, new_path: str) -> str:
    if not files[0].endswith(".txt"):
        return files

    new_files = []
    for file in files:
        new_file = file.split(".")[0] + ".txt"
        new_file = os.path.join(new_path, new_file)
        new_files.append(new_file)
    return new_files


def move_files(folders: list, new_path: str) -> list:
    os.makedirs(new_path, exist_ok=True)
    src_files_path = []
    for folder in folders:
        files = os.listdir(folder)
        files = [os.path.join(folder, file) for file in files]
        new_files = convert_txt_file_name(files, new_path)
        [shutil.copy(file, new_path) for file, new_file in zip(files, new_files)]
        src_files_path += files
    return src_files_path


def create_yolo_directory(src_path: str, new_path: str) -> list:
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    os.makedirs(new_path, exist_ok=True)

    src_files_path = []
    for folder in os.listdir(src_path):
        new_folder_path = os.path.join(new_path, folder)
        folder_path = os.path.join(src_path, folder)
        class_folders = os.listdir(folder_path)
        class_folders = [
            os.path.join(folder_path, class_folder) for class_folder in class_folders
        ]
        src_files_path += move_files(class_folders, new_folder_path)
    print("Directory created successfully")
    return src_files_path


def convert_label(file_path: str, class_id: str, image_size: tuple) -> None:
    with open(file_path, "r") as f:
        lines = f.readlines()
    lines = lines[1:]

    new_lines = []
    for line in lines:
        line = line.split(" ")
        # Calculate xywh
        x_center = (float(line[1]) + float(line[3])) / 2
        y_center = (float(line[2]) + float(line[4])) / 2
        width = float(line[3]) - float(line[1])
        height = float(line[4]) - float(line[2])

        # Normalize
        x_center /= image_size[1]
        y_center /= image_size[0]
        width /= image_size[1]
        height /= image_size[0]

        new_line = f"{class_id} {x_center} {y_center} {width} {height}"
        new_lines.append(new_line)

    with open(file_path, "w") as f:
        f.write("\n".join(new_lines))
    return


def convert_labels_to_yolo(new_path: str, class_path: str, src_files_path: str) -> None:
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

    # Get image size in a dictionary
    images_size = {}
    for file in src_files_path:
        print(file)
        image_name = os.path.basename(file).split(".")[0]
        image = cv2.imread(file)
        images_size[image_name] = image.shape[:2]

    # Convert labels to yolo format
    label_files = os.listdir(new_path)
    for file in label_files:
        file_name = file.split(".")[0]
        class_id = class_dict[file_name][LABEL_CLASS]
        image_size = images_size[file_name]
        convert_label(file, class_id, image_size)
    print("Labels converted successfully")


def convert_dataset_to_yolo(src_path: str, new_path: str, class_list_path: str) -> None:
    src_files_path = create_yolo_directory(src_path, new_path)
    convert_labels_to_yolo(new_path, class_list_path, src_files_path)
    # images_to_png(new_path)


def main():
    src_path = "/home/matheus/Downloads/ExDark"
    new_path = "/home/matheus/Downloads/yolo_ExDark"
    class_list_path = "/home/matheus/Downloads/imageclasslist.txt"
    convert_dataset_to_yolo(src_path, new_path, class_list_path)


if __name__ == "__main__":
    main()
