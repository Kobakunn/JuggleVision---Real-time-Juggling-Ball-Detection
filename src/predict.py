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

TEST_DIR = PROJECT_ROOT / "data" / "dataset" / "images" / "test"

RUNS_DIR = PROJECT_ROOT / "runs" / "detect"


model = YOLO(str(MODEL_PATH))

results = model.predict(
    source=str(TEST_DIR),
    device="cpu",
    save=True,
    project=str(RUNS_DIR),
    name="predict",
)