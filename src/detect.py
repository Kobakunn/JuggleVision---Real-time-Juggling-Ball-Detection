from pathlib import Path
import random

import cv2
from pythonosc.udp_client import SimpleUDPClient
from ultralytics import YOLO


# =========================
# パス設定
# =========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "detect"
    / "train"
    / "weights"
    / "best.pt"
)


# =========================
# YOLOモデル
# =========================

model = YOLO(str(MODEL_PATH))


# =========================
# OSC設定
# =========================

OSC_IP = "127.0.0.1"
OSC_PORT = 8000

client = SimpleUDPClient(
    OSC_IP,
    OSC_PORT,
)


# =========================
# カメラ
# =========================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("カメラを開けませんでした。")
    exit()


# =========================
# 光エフェクト
# =========================

def draw_glow(
    frame,
    center_x,
    center_y,
    size,
):

    center = (
        int(center_x),
        int(center_y),
    )


    # 外側の光

    overlay = frame.copy()

    cv2.circle(
        overlay,
        center,
        int(size * 1.8),
        (255, 255, 255),
        -1,
    )

    cv2.addWeighted(
        overlay,
        0.05,
        frame,
        0.95,
        0,
        frame,
    )


    # 中間の光

    overlay = frame.copy()

    cv2.circle(
        overlay,
        center,
        int(size * 1.3),
        (255, 255, 255),
        -1,
    )

    cv2.addWeighted(
        overlay,
        0.08,
        frame,
        0.92,
        0,
        frame,
    )

def draw_fire(
    frame,
    center_x,
    center_y,
    size,
):
    center_x = int(center_x)
    center_y = int(center_y)

    # =========================
    # 炎の大きさ
    # =========================

    fire_height = max(
        15,
        int(size * 1.5)
    )

    fire_width = max(
        8,
        int(size * 0.8)
    )


    # =========================
    # 炎専用のレイヤー
    # =========================

    fire = frame.copy()

    # 炎を描くためのマスク
    mask = frame.copy()

    # 真っ黒にする
    mask[:] = 0


    # =========================
    # 炎の粒
    # =========================

    for _ in range(8):

        x = center_x + random.randint(
            -fire_width,
            fire_width,
        )

        y = center_y + random.randint(
            -fire_height,
            fire_height // 2,
        )

        radius = random.randint(
            max(2, int(size * 0.1)),
            max(3, int(size * 0.3)),
        )

        color = random.choice(
            [
                (0, 0, 255),       # 赤
                (0, 100, 255),     # オレンジ
                (0, 200, 255),     # 黄色
            ]
        )

        cv2.circle(
            mask,
            (x, y),
            radius,
            color,
            -1,
        )


    # =========================
    # 炎だけをぼかす
    # =========================

    mask = cv2.GaussianBlur(
        mask,
        (0, 0),
        sigmaX=max(
            2,
            size * 0.15,
        ),
    )


    # =========================
    # 炎だけを合成
    # =========================

    cv2.addWeighted(
        frame,
        1.0,
        mask,
        0.5,
        0,
        frame,
    )


# =========================
# メインループ
# =========================

while True:

    ret, frame = cap.read()

    if not ret:

        print(
            "フレームを取得できませんでした。"
        )

        break


    # =========================
    # YOLO Tracking
    # =========================

    results = model.track(
        source=frame,
        device="cpu",
        conf=0.5,
        persist=True,
        verbose=False,
    )

    result = results[0]


    # =========================
    # ボール情報
    # =========================

    balls = []


    if result.boxes is not None:

        for box in result.boxes:

            # -------------------------
            # Bounding Box
            # -------------------------

            x1, y1, x2, y2 = (
                box.xyxy[0].tolist()
            )


            # -------------------------
            # 中心座標
            # -------------------------

            center_x = (
                x1 + x2
            ) / 2

            center_y = (
                y1 + y2
            ) / 2


            # -------------------------
            # サイズ
            # -------------------------

            width = x2 - x1
            height = y2 - y1

            size = max(
                width,
                height,
            )


            # -------------------------
            # Confidence
            # -------------------------

            confidence = float(
                box.conf[0]
            )


            # -------------------------
            # Tracking ID
            # -------------------------

            if box.id is not None:

                track_id = int(
                    box.id[0]
                )

            else:

                track_id = -1


            # -------------------------
            # 保存
            # -------------------------

            balls.append(
                [
                    track_id,
                    center_x,
                    center_y,
                    width,
                    height,
                    confidence,
                ]
            )


            # =========================
            # エフェクト
            # =========================

            # 光

            draw_glow(
                frame,
                center_x,
                center_y,
                size,
            )

            # 炎
            draw_fire(
                frame,
                center_x,
                center_y,
                size,
            )


            # =========================
            # Bounding Box
            # =========================

            x1_int = int(x1)
            y1_int = int(y1)
            x2_int = int(x2)
            y2_int = int(y2)

            cv2.rectangle(
                frame,
                (
                    x1_int,
                    y1_int,
                ),
                (
                    x2_int,
                    y2_int,
                ),
                (0, 255, 0),
                2,
            )


            # =========================
            # 中心点
            # =========================

            cv2.circle(
                frame,
                (
                    int(center_x),
                    int(center_y),
                ),
                5,
                (0, 0, 255),
                -1,
            )


            # =========================
            # ID
            # =========================

            cv2.putText(
                frame,
                f"ID: {track_id}",
                (
                    x1_int,
                    y1_int - 10,
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )


    # =========================
    # 最大3個
    # =========================

    balls = balls[:3]


    # =========================
    # OSCデータ
    # =========================

    osc_data = [
        len(balls)
    ]


    for ball in balls:

        track_id = ball[0]
        center_x = ball[1]
        center_y = ball[2]
        width = ball[3]
        height = ball[4]
        confidence = ball[5]


        osc_data.extend(
            [
                track_id,
                center_x,
                center_y,
                width,
                height,
                confidence,
            ]
        )


    # =========================
    # Processingへ送信
    # =========================

    client.send_message(
        "/balls",
        osc_data,
    )


    # =========================
    # カメラ表示
    # =========================

    cv2.imshow(
        "JuggleVision - YOLO Tracking",
        frame,
    )


    # =========================
    # 終了
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


cap.release()

cv2.destroyAllWindows()