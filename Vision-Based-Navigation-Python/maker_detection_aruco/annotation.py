import cv2
import numpy as np

def annotate(image, corners, ids):
    # VISUALISATION
    # Annotate and save the image if markers are detected
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
        cv2.imwrite("./annotated_images/detected_markers.png", image)
        print(f"Annotated image saved")
    else:
        print("No markers detected.")

    return