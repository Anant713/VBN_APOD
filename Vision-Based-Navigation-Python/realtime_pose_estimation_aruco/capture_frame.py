import os
from picamera2 import Picamera2
import time
import cv2
import numpy as np

def capture_frame():
    """
    Continuously captures frames from the Raspberry Pi Camera v2.

    Yields:
        frame (numpy.ndarray): The captured frame in RGB format.
    """
    picam = Picamera2()
    # Configure for video mode with reduced resolution
    video_resolution = (640, 480)
    config = picam.create_video_configuration(main={"size": video_resolution})
    picam.configure(config)

    picam.start()

    try:
        while True:
            frame = picam.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Saving in temporary buffer for videostreaming
            #cv2.imwrite("/tmp/image.jpeg",frame)
            
            yield frame
    finally:
        picam.stop()
