import os
import shutil
from PIL import Image

# 0 - labels
# 1 - light
# 2 - in/out
LABEL_CLASS = 0


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
        x, y, w, h = line[1], line[2], line[3], line[4]
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


def convert_labels_to_yolo(new_path: str, class_path: str) -> None:
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

    # Convert labels to yolo format
    image_files = os.listdir(os.path.join(new_path, "images"))
    label_files = os.listdir(os.path.join(new_path, "labels"))
    for image_file, label_file in zip(image_files, label_files):
        image = Image.open(image_file)
        width, height = image.size
        
        file_name = label_file.split(".")[0]
        class_id = class_dict[file_name][LABEL_CLASS]
        
        convert_label(os.path.join(new_path,"labels",label_file), class_id, (width, height))

    print("Labels converted successfully")


def images_to_jpg(dir_path: str) -> None:
    for image in os.listdir(dir_path):
        if image.endswith(".jpg"):
            continue
        image_path = os.path.join(dir_path, image)
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert('RGB')
        new_image_path = image_path.split(".")[0] + ".jpg"
        img.save(new_image_path)
    print("Images converted successfully")


def image_enhancement(dir_path: str) -> None:
    pass


def convert_dataset_to_yolo(src_path: str, new_path: str, class_list_path: str, enhancement_images: bool = False) -> None:
    create_yolo_directory(src_path, new_path)

    images_to_jpg(os.path.join(new_path, "images"))
    if enhancement_images:
        image_enhancement(os.path.join(new_path, "images"))

    convert_labels_to_yolo(new_path, class_list_path)


def main():
    src_path = "/home/matheus/Downloads/ExDark"
    new_path = "/home/matheus/Downloads/yolo_ExDark"
    class_list_path = "/home/matheus/Downloads/imageclasslist.txt"
    convert_dataset_to_yolo(src_path, new_path, class_list_path)


if __name__ == "__main__":
    main()
