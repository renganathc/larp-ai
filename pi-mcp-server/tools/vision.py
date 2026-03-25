from instances import mcp, picam2
import cv2
import requests
import time
import concurrent.futures

CV_SERVER_URL = "http://10.222.138.220:5001/detect"

CAMERA_CONFIGS = [
    {"AnalogueGain": 7.0, "ExposureTime": 17000, "Brightness": 0.48},
    {"AnalogueGain": 8.0, "ExposureTime": 30000, "Brightness": 0.4},
    {"AnalogueGain": 8.0, "ExposureTime": 24000, "Brightness": 0.4},
    {"AnalogueGain": 8.0, "ExposureTime": 40000},
    {}
]


def capture_image(config):

    picam2.set_controls(config)

    time.sleep(0.2)

    frame = picam2.capture_array()
    _, buffer = cv2.imencode(".jpg", frame)

    return buffer.tobytes()


def send_to_cv(image_bytes):
    try:
        files = {
            "file": ("frame.jpg", image_bytes, "image/jpeg")
        }

        response = requests.post(CV_SERVER_URL, files=files, timeout=7)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("Error:", str(e))
        return {"objects": [], "count": 0}


def merge_results(results):
    merged = {}

    for r in results:
        for obj in r.get("objects", []):
            name = obj if isinstance(obj, str) else obj.get("name")
            conf = 1.0 if isinstance(obj, str) else obj.get("confidence", 0)

            if name not in merged or conf > merged[name]:
                merged[name] = conf

    return list(merged.keys())


@mcp.tool()
def list_objects_in_image():
    """
    List all objects using multiple camera settings for better detection.
    """

    images = []
    for cfg in CAMERA_CONFIGS:
        img = capture_image(cfg)
        images.append(img)

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_to_cv, img) for img in images]
        for f in futures:
            results.append(f.result())

    final_objects = merge_results(results)

    return {
        "objects": final_objects,
        "count": len(final_objects),
        "unmerged_object_array": results
    }