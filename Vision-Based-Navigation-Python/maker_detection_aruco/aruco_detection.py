import cv2
import numpy as np

def aruco_detection(image):
    """
    A aruco detection function

    Args:
        image (numpy.ndarray): The input image to detect ArUco markers in.
    Returns:
        tuple: A tuple containing the corners (list of corner points) and ids (list of detected ArUco marker IDs).
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the ArUco dictionary and detector parameters
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    # Create the ArUco detector
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters = parameters)

    # Print the detected markers
    print("Detected markers:", ids)

    return corners,ids