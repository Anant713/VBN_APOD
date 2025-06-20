import cv2
import numpy as np

def process(raw_image,camMatrix,distCoeff):

    height, width = raw_image.shape[:2]
    camMatrixNew, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoeff, (width, height), 1, (width, height))
    image = cv2.undistort(raw_image, camMatrix, distCoeff, None, camMatrixNew)

    print("Image processed")
    return image