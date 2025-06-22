import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define image size
img_width, img_height = 3280, 2464
background_color = 0  # Black background

# Define 3D points of markers in millimeters
markers_3D = np.array([
    [20, 0, 10],
    [0, 20, 10],
    [-20, 0, 10],
    [0, -20, 10],
    [0, 0, 5]
], dtype=np.float32)

# Camera intrinsics
focal_length = 2590
image_center = (img_width // 2, img_height // 2)
camera_matrix = np.array([
    [focal_length, 0, image_center[0]],
    [0, focal_length, image_center[1]],
    [0, 0, 1]
], dtype=np.float32)

translation_vector = np.array([[0], [0], [50]], dtype=np.float32)  # In mm
dist_coeffs = np.zeros((4, 1), dtype=np.float32)

# Rotation range (degrees)
angles = np.linspace(-30, 30, 60)  # 60 frames

frames = []

fig = plt.figure(figsize=(10, 7))

def generate_frame(i):
    plt.clf()
    theta_x = np.radians(angles[i])
    theta_y = np.radians(angles[i] * 0.5)  # Half swing
    theta_z = np.radians(angles[i] * 0.3)  # Smaller swing

    # Convert Euler angles to a rotation vector
    R_vec, _ = cv2.Rodrigues(np.array([theta_x, theta_y, theta_z]))

    # Create blank image
    image = np.full((img_height, img_width), background_color, dtype=np.uint8)

    # Project points
    image_points, _ = cv2.projectPoints(markers_3D, R_vec, translation_vector, camera_matrix, dist_coeffs)

    for point in image_points:
        x, y = int(point[0][0]), int(point[0][1])
        if 0 <= x < img_width and 0 <= y < img_height:
            cv2.circle(image, (x, y), 20, 255, -1)

    # Apply blur
    image = cv2.GaussianBlur(image, (11, 11), 20)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Plot current frame
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    plt.title(f"Frame {i+1}/{len(angles)}")

    # Add green annotation for angles (in degrees)
    angle_text = (
        f"Theta X: {np.degrees(theta_x):.1f}°\n"
        f"Theta Y: {np.degrees(theta_y):.1f}°\n"
        f"Theta Z: {np.degrees(theta_z):.1f}°"
    )
    plt.text(100, img_height -400, angle_text, color='lime', fontsize=12,
             verticalalignment='top', fontweight='bold')
    


ani = animation.FuncAnimation(fig, generate_frame, frames=len(angles), interval=100, repeat=True)
# Optional: Save animation as video or gif
ani.save("camera_rotation.gif", writer="pillow", fps=10)
plt.show()

# ani.save("camera_rotation.mp4", writer="ffmpeg", fps=10)
