from ultralytics import YOLO

SEED = 42


def main():
    model = YOLO("yolov8n.pt")
    data_path = (
        "/home/matheusloiola/Documents/cnpq-caption-ia/project/datasets/caption.yaml"
    )
    results = model.train(
        data=data_path, epochs=40, imgsz=512, project="dataset_lvis_voc", seed=42,
        cache=True, batch=8
    )
    results.save()


if __name__ == "__main__":
    main()
