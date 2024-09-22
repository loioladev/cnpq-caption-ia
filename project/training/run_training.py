import argparse

from yolo_configs import train_detection_model, train_in_out_model, train_light_model

function_dict = {
    "light": train_light_model,
    "in_out": train_in_out_model,
    "detection": train_detection_model,
}


def create_parser() -> argparse.ArgumentParser:
    """Create a parser for the command line arguments"""
    parser = argparse.ArgumentParser(
        description="Train a YOLO class model for light classification"
    )
    parser.add_argument("dataset_path", type=str, help="Path to the dataset")
    parser.add_argument("model", type=str, help="Path to the model or the model name")
    parser.add_argument(
        "training",
        type=str,
        help="Problem to train",
        choices=["light", "in_out", "detection"],
    )
    parser.add_argument("--resume", action="store_true", help="Resume training")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    train_function = function_dict[args.training]
    train_function(args.dataset_path, args.model, args.resume)


if __name__ == "__main__":
    main()
