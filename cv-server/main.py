from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

app = FastAPI()

def fake_detect(image):
    return [
        {"label": "bottle", "x": 120, "y": 200},
        {"label": "person", "x": 300, "y": 180}
    ]

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "invalid image"}

    detections = fake_detect(image)

    return {
        "objects": detections,
        "count": len(detections)
    }