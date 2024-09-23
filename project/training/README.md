# Training directory

This directory contains the training scripts and configurations for the object detection and classification models.

## Running the training

To run the training, you can use the following command:

```bash
python3 run_training <dataset_path> <model> <training> [--resume]
```

Where:
- `<dataset_path>` is the path to the dataset directory.
- `<model>` is the model to be used or a path to a custom model.
- `<training>` is the training problem to be solved.
- `--resume` is an optional flag to resume the training from a checkpoint.

## Training results

This directory contains the training results for the models. The results are stored in the folder `runs` and are organized by the training problem and the model used. The folders contain the training logs and the training configuration.

- **Iteration Zero**: Models trained using the LVIS dataset and the VOC dataset with YOLOv8 model.
- **Iteration One**: Models trained using the LVIS dataset, the VOC dataset, and the OpenImages dataset with YOLOv8 model.
- **Iteration Two**: Models trained using the LVIS dataset, the VOC dataset with YOLOv8 model.
- **Iteration Three**: Models trained using the ExDark dataset for object detection with YOLOv10 model.
- **Iteration Four**: Models trained using the ExDark dataset for luminance classification with YOLOv8 for classification model.
- **Iteration Five**: Models trained using the ExDark dataset for indoor and outdoor classification with YOLOv8 for classification model.
