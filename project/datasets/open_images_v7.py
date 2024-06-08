from ultralytics.utils import Path, get_ubuntu_version, is_ubuntu
from ultralytics.utils.checks import check_requirements, check_version

check_requirements("fiftyone")
if is_ubuntu() and check_version(get_ubuntu_version(), ">=22.04"):
    check_requirements("fiftyone-db-ubuntu2204")

import fiftyone as fo
import fiftyone.zoo as foz

SAMPLES = 10000


def download_dataset(
    split: str, dataset_dir: str, name: str, train_split: bool
) -> foz.ZooDataset:
    """
    Download subset of Open Images dataset using FiftyOne Zoo. The complete
    dataset can be downloaded with these parameters in the function:
    max_samples=(1743042 if train else 41620)
    :param split: "train" or "validation"
    :param dataset_dir: directory to save the dataset
    :param name: dataset name
    :param train_split: if the split is the training one
    :return: FiftyOne Zoo dataset
    """
    samples = SAMPLES if train_split else round(SAMPLES * 0.1)
    dataset = foz.load_zoo_dataset(
        name,
        split=split,
        label_types=["detections"],
        dataset_dir=Path(dataset_dir) / "fiftyone" / name,
        max_samples=samples
    )
    return dataset


def export_dataset(
    dataset: foz.ZooDataset, dataset_dir: str, dataset_name: str, split: str, classes
) -> None:
    """
    Export dataset to YOLOv5 format. The dataset is exported to the directory
    dataset_dir/dataset_name/split
    :param dataset: FiftyOne Zoo dataset
    :param dataset_dir: directory to save the dataset
    :param dataset_name: dataset name
    :param split: "train" or "validation"
    :param classes: list of classes
    """
    dataset.export(
        export_dir=str(Path(dataset_dir) / dataset_name),
        dataset_type=fo.types.YOLOv5Dataset,
        label_field="ground_truth",
        split="val" if split == "validation" else split,
        classes=classes,
        overwrite=split == "train"
    )
    return


def main() -> None:
    """Main function to download and export Open Images dataset"""
    dataset_dir = "/media/matheus/RAIDER XI/cnpq"
    dataset_name = "open-images-v7"
    for split in ["train", "validation"]:
        train_split = split == "train"
        dataset = download_dataset(split, dataset_dir, dataset_name, split)
        if train_split:
            classes = dataset.default_classes
        export_dataset(dataset, dataset_dir, dataset_name, split, classes)


if __name__ == "__main__":
    main()
