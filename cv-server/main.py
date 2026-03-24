from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from ultralytics import YOLO
import torch
import threading
import uuid
import time

app = FastAPI()

if torch.cuda.is_available():
    DEVICE = "cuda"
elif torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"

print(f"[INFO] Using device: {DEVICE}")

model = YOLO("yolov8x.pt")

def show_detections(image, detections):

    window_name = f"Detections_{uuid.uuid4().hex[:8]}"

    for obj in detections:
        label = obj["label"]
        conf = obj["confidence"]
        bbox = obj["bbox"]

        x1, y1 = bbox["x1"], bbox["y1"]
        x2, y2 = bbox["x2"], bbox["y2"]

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        text = f"{label} {conf:.2f}"
        y_text = max(y1 - 10, 10)

        cv2.putText(
            image,
            text,
            (x1, y_text),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    cv2.imshow(window_name, image)
    cv2.waitKey(1)

    def close_window():
        time.sleep(10)
        cv2.destroyWindow(window_name)

    threading.Thread(target=close_window, daemon=True).start()

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "invalid image"}

    results = model(image, device=DEVICE)

    detections = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "label": label,
                "confidence": conf,
                "bbox": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                }
            })

    show_detections(image, detections)

    return {
        "objects": detections,
        "count": len(detections)
    }