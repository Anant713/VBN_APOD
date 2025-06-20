import cv2
import numpy as np

# Define the dictionary we want to use
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Generate a marker
marker_id = 40
marker_size = 500  # Size in pixels
border_size = 20  # Size of the padding around the marker

# Generate the marker
marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size, marker_image)

# Add padding (quiet zone) around the marker
padded_size = marker_size + 2 * border_size
padded_image = np.ones((padded_size, padded_size), dtype=np.uint8) * 255  # White padding
padded_image[border_size:border_size + marker_size, border_size:border_size + marker_size] = marker_image

# Save the padded marker
cv2.imwrite(f'marker_{marker_id}_{marker_size}.png',padded_image)
print("ArUco marker with padding saved")