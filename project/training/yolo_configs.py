from ultralytics import YOLO

SEED = 42


def train_detection_model(dataset_path: str, model: str, resume: bool) -> None:
    """
    Train a YOLO class model for detection

    :param dataset_path: The path to the dataset
    :param model: The path to the model or the model name
    :param resume: Resume training
    """
    model = YOLO(model)
    results = model.train(
        data=dataset_path,
        resume=resume,
        project="datasets_exdark",
        name="large_enhanced",
        epochs=125,
        imgsz=640,
        batch=8,
        cache=True,
        seed=SEED,
        patience=50,
        workers=8,
        plots=True,
    )

    return results


def train_light_model(dataset_path: str, model: str, resume: bool) -> None:
    """
    Train a YOLO class model for light classification

    :param dataset_path: The path to the dataset
    :param model: The path to the model or the model name
    :param resume: Resume training
    """
    model = YOLO(model)
    results = model.train(
        data=dataset_path,
        epochs=30,
        imgsz=640,
        project="classification_light",
        seed=SEED,
        batch=4,
        cache=True,
        resume=resume,
    )

    return results


def train_in_out_model(dataset_path: str, model: str, resume: bool) -> None:
    """
    Train a YOLO class model for in/out classification

    :param dataset_path: The path to the dataset
    :param model: The path to the model or the model name
    :param resume: Resume training
    """
    pass
