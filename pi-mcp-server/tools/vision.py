from instances import mcp, picam2
import cv2
import requests

CV_SERVER_URL = "http://localhost:5000/detect"


def capture_image():
    print("[CAMERA] Capturing image")

    frame = picam2.capture_array()
    
    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()


def send_to_cv(image_bytes):
    print("Sending image to CV server...")

    try:
        files = {
            "file": ("frame.jpg", image_bytes, "image/jpeg")
        }

        response = requests.post(CV_SERVER_URL, files=files, timeout=7)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("Error :", str(e))
        return {"objects": [], "count": 0}


@mcp.tool()
def list_objects_in_image():
    """
    List all objects currently visible in the camera frame.
    """
    image = capture_image()
    result = send_to_cv(image)

    detected = result.get("objects", [])

    return {
        "objects": detected,
        "count": len(detected)
    }