# VISION BASED NAVIGATION

Check calibration directory for camera calibration scripts
### DIRECTORY STRUCTURE

### REQUIREMENTS
- Raspberry Pi 4B
- Raspberry Pi Camera Module 2
- OpenCV version 4.6.0
- Numpy version 1.24.2

### PINHOLE CAMERA MODEL
![Pinhole Camera Model](/images/pinhole_camera_model.png) \
Camera frame axis definition
- Z-axis: Points along the optical axis of the camera (forward, towards the scene the camera is observing).
- X-axis: Typically points to the right (horizontal) in the camera's image plane.
- Y-axis: Points downward in the camera's image plane (vertical).

### ArUco Marker Frame
![ArUco Marker Frame](/images/ArUco%20marker%20frame.png)
ArUco marker frame axis definition
- Z-axis (blue): Points outwards 
- X-axis (red): Points to the right 
- Y-axis (green): Points upwards