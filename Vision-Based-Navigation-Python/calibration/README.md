## CAMERA CALIBRATION

- Display pattern.png on a external monitor
- Check if chessboard is in FOV of camera with 
```bash 
rpicam-hello -t 0
```
- run cam_capture.py script. It takes 10 images continuously with wait time and saves it in calibration_images. Note that the calibration images should be taken in different orientations to avoid deenerate cases and entire chessboard should be visible.
- run camcal.py script which will print the camera intrinsic matrix and the reconstruction projection error on the terminal. It saves the camera intrinsic, extrinsic matrices, distortion coefficients and projection error in an .npz file
- To acces the data from .npz file run npz_extract.py script


