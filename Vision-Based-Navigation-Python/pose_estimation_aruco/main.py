import cv2
import numpy as np
from capture_image import capture_image # Comment if using on PC
from processing import process
import aruco_detection as ad
from pose_estimation import estimate_pose
from annotation import annotate
from frame_transformations import PRV2Euler, PRV2PRV_deg

# CAMERA PARAMETERS
global camMatrix, distCoeff
# MARKER PARAMETERS
global marker_length

camMatrix = np.array([[2593,0,1614],[0,2588,1213],[0,0,1]], dtype=np.float32)
distCoeff = np.array([[ 2.18984921e-01,-5.80493965e-01,1.15200278e-04,-2.04177566e-03,4.48611005e-01]])

marker_length = 0.05  # [m]

# CAPTURE
# Load the image
#raw_image = cv2.imread('./raw_images/image1.jpg') # To read image on PC
raw_image = capture_image() # To capture image from hardware
cv2.imwrite('raw_image.jpg', raw_image)

# PROCESSING
image = process(raw_image,camMatrix,distCoeff)
cv2.imwrite('processed_image.jpg', image)

# ARUCO DETECTION
corners, ids = ad.aruco_detection(image)

# POSE ESTIMATION
pose_data = estimate_pose(corners, ids, camMatrix, distCoeff, marker_length)

print(pose_data)

# PRINT OUTPUTS FOR INTUITION
for marker_id, (rvec, tvec) in pose_data.items():
    print(f"Marker ID: {marker_id}")
    
    # Translation
    # Ensure the rvec is a numpy array
    tvec = np.array(tvec).flatten()
    x,y,z = tvec
    print(f"x [mm] : {x*1000:.3f}")
    print(f"y [mm] : {y*1000:.3f}")
    print(f"z [mm] : {z*1000:.3f}")

    # Convert rotation vector to unit vector and angle
    unit_vector, angle_deg = PRV2PRV_deg(rvec)
    print(f"Unit Vector: {unit_vector}")
    print(f"Rotation Angle (in degrees): {angle_deg}")
    
    # Convert rotation vector to Roll, Pitch, Yaw angles
    roll, pitch, yaw = PRV2Euler(rvec)
    print(f"Roll: {roll:.3f}°")
    print(f"Pitch: {pitch:.3f}°")
    print(f"Yaw: {yaw:.3f}°")

# VISUALISATION
annotate(image,corners,ids,camMatrix,marker_length,pose_data)

# FRAME TRANSFORMATIONS FOR DOCKING
pass