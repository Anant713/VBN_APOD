
# Camera Pose Dataset Usage Guide

## Dataset Structure
```
camera_pose_dataset/
├── images/                     # Synthetic images (PNG format)
│   ├── image_000000.png       # Image files named by sample ID
│   └── ...
├── annotations/                # Ground truth pose data (JSON format)  
│   ├── pose_000000.json       # Individual pose annotations
│   └── ...
├── dataset.csv                 # Complete dataset in CSV format
├── all_poses.json             # All pose data in single JSON file
└── dataset_summary.json       # Dataset statistics and metadata
```

## Loading the Dataset

### Python Example:
```python
import pandas as pd
import json
import cv2

# Load the complete dataset
df = pd.read_csv('camera_pose_dataset/dataset.csv')

# Load a specific image and its annotation
sample_id = 0
image_path = f'camera_pose_dataset/images/image_{sample_id:06d}.png'
annotation_path = f'camera_pose_dataset/annotations/pose_{sample_id:06d}.json'

# Load image
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Load ground truth pose
with open(annotation_path, 'r') as f:
    pose_data = json.load(f)

# Extract pose parameters
roll = pose_data['pose']['roll_deg']
pitch = pose_data['pose']['pitch_deg'] 
yaw = pose_data['pose']['yaw_deg']
tx = pose_data['pose']['tx_mm']
ty = pose_data['pose']['ty_mm']
tz = pose_data['pose']['tz_mm']
```

## Ground Truth Data Format

Each annotation JSON contains:
- `sample_id`: Unique identifier
- `pose`: Camera pose in degrees and millimeters
  - `roll_deg`, `pitch_deg`, `yaw_deg`: Euler angles
  - `tx_mm`, `ty_mm`, `tz_mm`: Translation vector
- `rotation_vector`: OpenCV rotation vector format
- `translation_vector`: OpenCV translation vector format
- `markers_2d`: 2D projections of 3D markers
- `markers_in_frame_count`: Number of visible markers
- `image_file`: Corresponding image filename

## Parameter Ranges (OpenCV Coordinate System)

- **Roll (X rotation)**: ±85° (camera tilt left/right)
- **Pitch (Y rotation)**: ±40° (camera tilt up/down)  
- **Yaw (Z rotation)**: ±40° (camera rotate left/right)
- **X translation**: ±1000mm (left/right movement)
- **Y translation**: ±1000mm (up/down movement)
- **Z translation**: 10-3000mm (forward/backward movement)

## Algorithm Testing Workflow

1. **Load dataset**: Use CSV for quick access or JSON for detailed annotations
2. **Filter samples**: Select subsets based on marker visibility or pose ranges
3. **Run your algorithm**: Process images and estimate poses
4. **Compare results**: Compare estimated poses with ground truth
5. **Evaluate accuracy**: Compute error metrics (position, rotation errors)

## Evaluation Metrics

Common metrics for pose estimation accuracy:
- **Translation Error**: ||t_estimated - t_ground_truth|| (mm)
- **Rotation Error**: Angular difference between rotation matrices (degrees)
- **Reprojection Error**: 2D distance between projected and detected markers (pixels)

## Dataset Filtering Examples

```python
# Filter samples with all markers visible
good_samples = df[df['markers_in_frame'] == 5]

# Filter by pose range (e.g., small rotations)
small_rotations = df[
    (abs(df['roll_deg']) < 30) & 
    (abs(df['pitch_deg']) < 20) & 
    (abs(df['yaw_deg']) < 20)
]

# Filter by distance range
close_range = df[(df['tz_mm'] >= 10) & (df['tz_mm'] <= 500)]
```

## Notes

- All coordinates are in OpenCV coordinate system (Right-Down-Forward)
- Images are grayscale with Gaussian-blurred marker spots
- Marker positions are at 20mm intervals around the origin
- Camera intrinsics: focal_length=2590px, no distortion
- Image resolution: 3280×2464 (OV5647 sensor)
