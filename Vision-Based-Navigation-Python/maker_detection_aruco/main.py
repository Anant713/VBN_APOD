import cv2
import numpy as np
from capture_image import capture_image # Comment if using on PC
from processing import process
import aruco_detection as ad
from annotation import annotate

# CAPTURE
# Load the image
#raw_image = cv2.imread('./raw_images/image1.jpg') # To read image on PC
raw_image = capture_image() # To capture image from hardware
cv2.imwrite('raw_image.jpg', raw_image)

# PROCESSING
image = process(raw_image)
cv2.imwrite('processed_image.jpg', image)

# ARUCO DETECTION
corners, ids = ad.aruco_detection(image)

# VISUALISATION
annotate(image,corners,ids)
