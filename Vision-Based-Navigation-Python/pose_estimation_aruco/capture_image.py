import os
from picamera2 import Picamera2
import time
import cv2
import numpy as np

def capture_image():
    """
    Captures a still image using the Raspberry Pi Camera v2.

    Returns:
        image (numpy.ndarray): The captured image in RGB format.
    """

    picam = Picamera2()
    # Set the maximum resolution
    max_resolution = (3280, 2464)  # Example for Camera Module v2
    config = picam.create_still_configuration(main={"size": max_resolution})
    picam.configure(config)

    picam.start()

    for i in range(3):
        print(f"{3-i}")
        time.sleep(1)

    # Capture the image as a numpy array
    image = picam.capture_array()

    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    # To save file and read again from that file
    # picam.capture_file("raw_image.jpg")
    # raw_image = cv2.imread('raw_image.jpg') 

    print("Captured")
    
    picam.stop()

    return image