import numpy as np
import cv2
import matplotlib.pyplot as plt

def euler_to_rvec(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Convert roll‑pitch‑yaw (deg) to a Rodrigues rotation vector."""
    rx, ry, rz = np.radians([roll, pitch, yaw])
    # Build rotation matrix Rz * Ry * Rx (Z‑YX convention)
    cz, sz = np.cos(rz), np.sin(rz)
    cy, sy = np.cos(ry), np.sin(ry)
    cx, sx = np.cos(rx), np.sin(rx)

    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])

    R = Rz @ Ry @ Rx
    rvec, _ = cv2.Rodrigues(R)
    return rvec


# Define image size
img_width, img_height = 3280, 2464  # OV5647 resolution
background_color = 0  # Black background for grayscale

# Create a blank grayscale image (8-bit)
image = np.zeros((img_height, img_width), dtype=np.uint8)
image[:] = background_color

# Define 3D points of markers in millimeters (w.r.t. pinhole)
markers_3D = np.array([
    [-55, 0, 0],    # Marker 1 (3m in front)
    [0, 55, 0],  # Marker 2 (right)
    [0, 0, -15],  # Marker 3 (up)
    # [50, 0, 30],
    # [-50,0,30]
], dtype=np.float32)

# Define camera intrinsic matrix (assuming focal length in pixels)
focal_length = 2714.286  # Pixels (adjust if needed)
# mx = 1000/1.12 # no. of pixels/mm in x direction
# my = 1000/1.12 # no. of pixels/mm in y direction
# fx = mx * focal_length
# fy = my * focal_length
image_center = (img_width // 2, img_height // 2)
camera_matrix = np.array([
    [focal_length, 0, image_center[0]],
    [0, focal_length, image_center[1]],
    [0, 0, 1]
], dtype=np.float32)

# Define camera rotation (Euler angles: pitch, yaw, roll in degrees)
xdeg = 0
ydeg = 30
zdeg = 0
theta_x, theta_y, theta_z = np.radians([xdeg, ydeg,zdeg])  # Rotation in X, Y, Z (in degrees)
#rotation_vector, _ = cv2.Rodrigues(np.array([theta_x, theta_y, theta_z]))  # Convert to rotation vector
rotation_vector = euler_to_rvec(xdeg, ydeg,zdeg)
print(rotation_vector)
# Define camera translation (moving camera in mm)
translation_vector = np.array([[0], [0], [3000]], dtype=np.float32)  # Shift right & down

# No distortion
dist_coeffs = np.zeros((4, 1), dtype=np.float32)

# Project 3D points to 2D image plane
image_points, _ = cv2.projectPoints(markers_3D, rotation_vector, translation_vector, camera_matrix, dist_coeffs)

# Apply Gaussian blur at projected points
for point in image_points:
    x, y = int(point[0][0]), int(point[0][1])
    if 0 <= x < img_width and 0 <= y < img_height:  # Ensure points are in frame
        cv2.circle(image, (x, y), 7, 255, -1)  # Draw filled white spots

# Apply Gaussian blur to spread intensities
image = cv2.GaussianBlur(image, (11, 11), 5)  # Adjust blur size & sigma

# Normalize & convert to 8-bit
image = image.clip(0, 255).astype(np.uint8)

# Display using plt (grayscale)
plt.figure(figsize=(10, 7))
plt.imshow(image, cmap="gray")
plt.axis("off")
plt.show()
#cv2.imwrite("projected_markers.png", image)

from PIL import Image
import numpy as np

# Load image
img_array = np.array(image)

# Save as true raw binary
with open('./simulated-image.raw', 'wb') as f:
    f.write(img_array.tobytes())
print (img_array.shape)

#Write in text file
with open("comparison.txt", "a", encoding="utf-8") as f:
    line = (
        f"expected,"
        f"{zdeg},"
        f"{xdeg},"
        f"{ydeg},"
        f"{translation_vector[2]},"
        f"{translation_vector[0]},"
        f"{translation_vector[1]}\n"
    )
    f.write(line)
