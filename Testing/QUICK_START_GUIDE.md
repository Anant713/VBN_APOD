# Camera Pose Dataset - Quick Start Guide

## What You Have

✅ **Complete Camera Pose Dataset** (500 samples)
- Synthetic images with 5 markers per image
- Ground truth poses in OpenCV coordinate system  
- Parameter ranges: ±85° roll, ±40° pitch/yaw, 10-3000mm distance
- Latin Hypercube Sampling for optimal coverage

✅ **Algorithm Testing Framework**
- PoseEstimationEvaluator class for easy testing
- Automatic accuracy calculation (translation & rotation errors)
- Batch evaluation and report generation
- Example code and usage templates

✅ **Documentation & Tools**
- Complete usage guides and README files
- Dataset analysis and visualization scripts
- Large dataset generation capability
- Comprehensive evaluation metrics

## Quick Start (3 Steps)

### Step 1: Load the Dataset
```python
import pandas as pd
df = pd.read_csv('camera_pose_dataset/dataset.csv')
print(f"Dataset: {len(df)} samples")
print(f"Good visibility: {len(df[df['markers_in_frame'] >= 4])} samples")
```

### Step 2: Test Your Algorithm
```python
from pose_estimation_evaluator import PoseEstimationEvaluator

# Initialize evaluator
evaluator = PoseEstimationEvaluator("camera_pose_dataset")

# Replace these with your actual algorithms
def your_marker_detection(image):
    # Your detection code here
    return detected_markers_2d

def your_pose_estimation(markers_2d):
    # Your pose estimation code here  
    return rotation_vector, translation_vector

# Test on 50 good samples
good_samples = df[df['markers_in_frame'] >= 4]['sample_id'].tolist()[:50]
results_df, stats = evaluator.evaluate_algorithm(
    sample_subset=good_samples,
    detection_func=your_marker_detection,
    pose_func=your_pose_estimation
)

# Generate report
report = evaluator.create_evaluation_report(results_df, stats)
print(report)
```

### Step 3: Analyze Results
The framework automatically calculates:
- Success rate (% of poses successfully estimated)
- Translation error (mm) - mean, median, std
- Rotation error (degrees) - mean, median, std  
- Performance by marker visibility
- Component-wise error analysis

## Dataset Structure

```
camera_pose_dataset/
├── images/                  # 500 PNG images (3280x2464)
│   ├── image_000000.png    # Sample images with markers
│   └── ...
├── annotations/             # Ground truth JSON files
│   ├── pose_000000.json    # Pose data for each image
│   └── ...
├── dataset.csv             # Complete dataset (easy to load)
├── all_poses.json          # All poses in single file
├── dataset_summary.json    # Dataset statistics
└── README.md              # Detailed usage guide
```

## Key Insights from Dataset Analysis

🎯 **Distance is Critical**: Camera distance (Z translation) has strongest impact on marker visibility (correlation = 0.78)

📊 **Distribution**: 
- 58% of samples have all 5 markers visible
- 40% have no markers visible (typically close distances)
- Sweet spot: 1500-3000mm distance for good visibility

🔧 **Testing Strategy**:
1. Start with samples where markers_in_frame >= 4
2. Test across different distance ranges
3. Evaluate robustness with challenging poses
4. Analyze failure cases for algorithm improvement

## Parameter Ranges (OpenCV Coordinate System)

| Parameter | Range | Description |
|-----------|-------|-------------|
| Roll (X rotation) | ±85° | Camera tilt around optical axis |
| Pitch (Y rotation) | ±40° | Camera tilt up/down |
| Yaw (Z rotation) | ±40° | Camera rotate left/right |
| X translation | ±1000mm | Left/right camera movement |
| Y translation | ±1000mm | Up/down camera movement |
| Z translation | 10-3000mm | Forward/backward movement |

## Advanced Usage

### Generate Larger Dataset
```bash
python generate_large_dataset.py --samples 2000 --method lhs --output big_dataset
```

### Filter by Difficulty
```python
# Easy poses (close, small rotations)
easy = df[(df['tz_mm'] < 500) & (abs(df['roll_deg']) < 30)]

# Hard poses (distant, large rotations)  
hard = df[(df['tz_mm'] > 2000) & (abs(df['roll_deg']) > 60)]

# Specific conditions
close_range = df[(df['tz_mm'] >= 10) & (df['tz_mm'] <= 500)]
```

### Custom Evaluation
```python
# Test specific sample
result = evaluator.test_algorithm_on_sample(sample_id=42)

# Test subset with specific conditions
subset_ids = df[df['markers_in_frame'] == 5]['sample_id'].tolist()
results_df, stats = evaluator.evaluate_algorithm(sample_subset=subset_ids)
```

## Next Steps

1. **Replace placeholder functions** in the evaluator with your actual algorithms
2. **Start testing** with samples that have good marker visibility (≥4 markers)
3. **Analyze performance** across different pose ranges and conditions
4. **Iterate and improve** your algorithms based on the results
5. **Generate larger datasets** if needed for comprehensive evaluation

## Support

- Check `README.md` in the dataset folder for detailed documentation
- Review `DATASET_SUMMARY.md` for complete technical details
- Use the example code in `pose_estimation_evaluator.py` as a starting point
- Modify parameters in the generator for custom datasets

---

**Ready to test your algorithm? Start with Step 1 above! 🚀**