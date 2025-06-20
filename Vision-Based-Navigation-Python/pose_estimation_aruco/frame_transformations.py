import numpy as np
import cv2

def PRV2PRV_deg(rvec):
    """
    Convert rotation vector to unit vector and rotation angle in degrees.
    
    Args:
        rvec (numpy.ndarray): Rotation vector (3x1 or 1x3).
    
    Returns:
        unit_vector (numpy.ndarray): Unit vector representing the axis of rotation.
        angle_deg (float): Rotation angle in degrees.
    """
    # Ensure the rvec is a numpy array
    rvec = np.array(rvec).flatten()

    # Calculate the angle (magnitude of the rotation vector)
    angle_rad = np.linalg.norm(rvec)  # Magnitude gives the angle in radians
    angle_deg = np.degrees(angle_rad)  # Convert to degrees

    # Calculate the unit vector (axis of rotation)
    if angle_rad != 0:
        unit_vector = rvec / angle_rad  # Normalize the rotation vector
    else:
        unit_vector = np.array([0, 0, 0])  # No rotation

    return unit_vector, angle_deg


def PRV2Euler(rvec):
    """
    Convert a rotation vector to roll, pitch, and yaw angles.
    
    Args:
        rvec (numpy.ndarray): Rotation vector (3x1 or 1x3).
    
    Returns:
        roll (float): Roll angle in degrees.
        pitch (float): Pitch angle in degrees.
        yaw (float): Yaw angle in degrees.
    """
    # Convert the rotation vector to a rotation matrix
    R, _ = cv2.Rodrigues(rvec)

    # Calculate roll, pitch, yaw from the rotation matrix
    sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)
    singular = sy < 1e-6  # Handle gimbal lock
    if not singular:
        roll = np.arctan2(R[2, 1], R[2, 2])  # Rotation around X-axis
        pitch = np.arctan2(-R[2, 0], sy)     # Rotation around Y-axis
        yaw = np.arctan2(R[1, 0], R[0, 0])   # Rotation around Z-axis
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = 0

    # Convert to degrees
    roll, pitch, yaw = np.degrees([roll, pitch, yaw])
    
    # Round the results to 3 decimal places
    roll = round(roll, 3)
    pitch = round(pitch, 3)
    yaw = round(yaw, 3)

    return roll, pitch, yaw


# Example usage
rvec = np.array([0.2, 0.1, 0.05])  # Example rotation vector

# Convert rotation vector to unit vector and angle
unit_vector, angle_deg = PRV2PRV_deg(rvec)
print(f"Unit Vector: {unit_vector}")
print(f"Rotation Angle (in degrees): {angle_deg}")

# Convert rotation vector to Roll, Pitch, Yaw
roll, pitch, yaw = PRV2Euler(rvec)
print(f"Roll: {roll}°")
print(f"Pitch: {pitch}°")
print(f"Yaw: {yaw}°")
