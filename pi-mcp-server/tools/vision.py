from mcp_instance import mcp
import requests

CV_SERVER_URL = "my ip"


def capture_image():
    print("Capturing image...")

    return b"fake_image_data"


def send_to_cv(image_bytes):
    print("Sending image to CV server...")

    try:
        files = {
            "image": ("frame.jpg", image_bytes, "image/jpeg")
        }

        response = requests.post(CV_SERVER_URL, files=files)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("Error :", str(e))
        return {"objects": []}


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