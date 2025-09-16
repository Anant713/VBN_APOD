import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Replace 'your_image.jpg' with your actual image filename
image = mpimg.imread('/home/anant/VBN/images/image_23_100um_sun.jpg')

plt.imshow(image)
plt.axis('off')  # Hide axes
plt.show()