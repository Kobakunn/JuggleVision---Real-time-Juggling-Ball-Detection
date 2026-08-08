import cv2
import os

video_path = "data/raw/videos/park/park_test.MOV"
save_dir = "data/dataset/images/test"

os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

frame_count = 0
save_count = 0

interval = 5  # 5フレームごと

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if frame_count % interval == 0:
        filename = f"{save_dir}/image_{save_count:04d}.jpg"
        cv2.imwrite(filename, frame)
        save_count += 1

    frame_count += 1

cap.release()

print(f"{save_count} images saved")