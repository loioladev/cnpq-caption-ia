# YAML Data Configuration Files

This directory contains YAML configuration files used for training **YOLO (You Only Look Once)** models. These files define the training parameters, such as paths to the datasets, hyperparameters, and model architecture.

## YAML Files

Each YAML file contains the configuration for a specific YOLO model.

### YAML Structure Fields

Each YAML file contains the following fields:

- **`train`**: Path to the training dataset.
- **`val`**: Path to the validation dataset.
- **`nc`**: Number of classes in the dataset.
- **`names`**: List of class names.
