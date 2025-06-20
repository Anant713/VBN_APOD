import cv2
import numpy as np

def estimate_pose(corners, ids, camera_matrix, dist_coeffs, marker_length):
    """
    Estimates pose of detected ArUco markers using solvePnP.

    Args:
        corners (list): List of corners of detected markers (in pixels).
        ids (list): IDs of the detected markers.
        camera_matrix (numpy.ndarray): Camera intrinsic parameters.
        dist_coeffs (numpy.ndarray): Distortion coefficients.
        marker_length (float): Physical side length of the ArUco marker in meters.

    Returns:
        dict: A dictionary where keys are marker IDs, and values are (rvec, tvec).
    """
    pose_data = {}

    # Define the 3D coordinates of the marker corners in the marker's frame (in meters)
    marker_points_3d = np.array([
        [-marker_length / 2,  marker_length / 2, 0],  # Top-left corner
        [ marker_length / 2,  marker_length / 2, 0],  # Top-right corner
        [ marker_length / 2, -marker_length / 2, 0],  # Bottom-right corner
        [-marker_length / 2, -marker_length / 2, 0]   # Bottom-left corner
    ], dtype=np.float32)

    if ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            # Get the 2D points for the current marker
            marker_points_2d = corners[i].reshape(-1, 2)

            # Use solvePnP to estimate the pose of the marker relative to the camera
            success, rvec, tvec = cv2.solvePnP(marker_points_3d, marker_points_2d, camera_matrix, None) # Lat argument is distCoeff which has already been removed from image
            if success:
                # Add the pose (rotation vector and translation vector) to the dictionary
                pose_data[marker_id] = (rvec, tvec)

    return pose_data
