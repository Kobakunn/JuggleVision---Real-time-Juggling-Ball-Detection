import cv2
import os


place_name = "indoor"
folder_name = "val"

video_path = f"../data/raw/videos/{place_name}/{place_name}_{folder_name}.MOV"
save_dir = f"../data/dataset/images/{folder_name}"

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
        filename = f"{save_dir}/{place_name}_{folder_name}_{save_count:04d}.jpg"
        cv2.imwrite(filename, frame)
        save_count += 1

    frame_count += 1

cap.release()

print(f"{save_count} images saved")