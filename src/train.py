from pathlib import Path

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_YAML = PROJECT_ROOT / "data" / "dataset" / "data.yaml"
RUNS_DIR = PROJECT_ROOT / "runs" / "detect"


model = YOLO("yolo11n.pt")

results = model.train(
    data=str(DATA_YAML),
    epochs=50,
    imgsz=640,
    batch=64,
    device="cpu",
    project=str(RUNS_DIR),
    name="train",
)