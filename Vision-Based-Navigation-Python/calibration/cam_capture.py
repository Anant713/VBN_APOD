import os
from picamera2 import Picamera2
import time

def capture_images():
    picam = Picamera2()
    # Set the maximum resolution
    max_resolution = (3280, 2464)  # Example for Camera Module v2
    config = picam.create_still_configuration(main={"size": max_resolution})
    picam.configure(config)

    picam.start()

    # Define the output directory
    output_dir = "./calibration_images"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, 11):
        file_name = os.path.join(output_dir, f"test{i}.jpg")
        print(f"Holding {file_name}...")
        time.sleep(2)
        picam.capture_file(file_name)
        print(f"Captured{file_name}...")
        time.sleep(1)  # Delay between captures

    picam.stop()

if __name__ == "__main__":
    capture_images()
