import cv2
import numpy as np

def annotate(image, corners, ids, camMatrix, marker_length, pose_data):
    """
    Annotates the image with detected ArUco markers and their axis vectors and saves the image
    
    Args:
        image (numpy.ndarray): Input image with detected ArUco markers.
        corners (list): List of corners of detected markers.
        ids (list): IDs of the detected markers.
        camera_matrix (numpy.ndarray): Camera intrinsic parameters.
        marker_length (float): Physical side length of the ArUco marker in meters.
    
    Returns:
        image (numpy.ndarray): Annotated image with axis vectors drawn.
    """
    if ids is not None:
        # Draw axis for each marker
        for marker_id, (rvec, tvec) in pose_data.items():
            # Draw the frame axes for the marker (3D axes drawn on the image)
            cv2.aruco.drawDetectedMarkers(image, corners, ids)

            # Draw the frame axes based on the marker's pose
            cv2.drawFrameAxes(image, camMatrix, None, rvec, tvec, marker_length / 2)
            cv2.aruco.drawDetectedMarkers(image, corners, ids)
            cv2.imwrite("./annotated_images/detected_markers.png", image)
            print(f"Annotated image saved")
    else:
        print("No markers detected.")

    return