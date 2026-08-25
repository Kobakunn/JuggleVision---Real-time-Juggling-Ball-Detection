from pathlib import Path

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "detect"
    / "train"
    / "weights"
    / "best.pt"
)

DATA_YAML = PROJECT_ROOT / "data" / "dataset" / "data.yaml"


model = YOLO(str(MODEL_PATH))

metrics = model.val(
    data=str(DATA_YAML),
    split="test",
    device="cpu",
)


print("\n=== Evaluation Results ===")
print(f"Precision : {metrics.box.mp:.4f}")
print(f"Recall    : {metrics.box.mr:.4f}")
print(f"mAP50     : {metrics.box.map50:.4f}")
print(f"mAP50-95  : {metrics.box.map:.4f}")