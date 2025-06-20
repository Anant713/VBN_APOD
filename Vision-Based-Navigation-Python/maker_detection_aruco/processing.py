import cv2
import numpy as np

global camMatrix, distCoeff

camMatrix = np.array([[2593,0,1614],[0,2588,1213],[0,0,1]])
distCoeff = np.array([[ 2.18984921e-01,-5.80493965e-01,1.15200278e-04,-2.04177566e-03,4.48611005e-01]])

def process(raw_image):

    height, width = raw_image.shape[:2]
    camMatrixNew, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoeff, (width, height), 1, (width, height))
    image = cv2.undistort(raw_image, camMatrix, distCoeff, None, camMatrixNew)

    print("Image processed")
    return image