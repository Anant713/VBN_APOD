from PIL import Image
import numpy as np

# Load the image
img = Image.open('/home/anant/VBN/images/image_23_100um_sun.jpg').convert('L')  # 'L' mode is grayscale

# Convert to numpy array
arr = np.array(img)

# Save as raw
arr.tofile('output.raw')