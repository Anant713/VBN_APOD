
import numpy as np
import pandas as pd
import json
import cv2
import os
from scipy.spatial.transform import Rotation as R

class PoseEstimationEvaluator:
    """
    Framework for evaluating pose estimation algorithms on the synthetic dataset.
    Provides loading, testing, and accuracy measurement tools.
    """

    def __init__(self, dataset_path="camera_pose_dataset"):
        """Initialize the evaluator with dataset path"""
        self.dataset_path = dataset_path
        self.df = pd.read_csv(os.path.join(dataset_path, "dataset.csv"))
        self.camera_matrix = np.array([
            [2590, 0, 1640],    # Focal length and center from original code
            [0, 2590, 1232],
            [0, 0, 1]
        ], dtype=np.float32)
        self.dist_coeffs = np.zeros((4, 1), dtype=np.float32)

        # 3D marker positions (same as in dataset generation)
        self.markers_3D = np.array([
            [0, 20, 0],    # Marker 1
            [0, 0, 20],    # Marker 2 
            [0, -20, 0],   # Marker 3
            [0, 0, -20],   # Marker 4
            [-20, 0, 0]    # Marker 5
        ], dtype=np.float32)

        print(f"Evaluator initialized with {len(self.df)} samples")

    def load_sample(self, sample_id):
        """Load a specific sample (image + ground truth)"""

        # Load image
        image_path = os.path.join(self.dataset_path, "images", f"image_{sample_id:06d}.png")
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Load ground truth
        annotation_path = os.path.join(self.dataset_path, "annotations", f"pose_{sample_id:06d}.json")
        with open(annotation_path, 'r') as f:
            ground_truth = json.load(f)

        return image, ground_truth

    def get_ground_truth_pose(self, sample_id):
        """Extract ground truth pose in standard format"""
        _, gt_data = self.load_sample(sample_id)

        # Extract pose parameters
        pose = {
            'roll_deg': gt_data['pose']['roll_deg'],
            'pitch_deg': gt_data['pose']['pitch_deg'], 
            'yaw_deg': gt_data['pose']['yaw_deg'],
            'tx_mm': gt_data['pose']['tx_mm'],
            'ty_mm': gt_data['pose']['ty_mm'],
            'tz_mm': gt_data['pose']['tz_mm'],
            'rotation_vector': np.array(gt_data['rotation_vector']),
            'translation_vector': np.array(gt_data['translation_vector']),
            'markers_visible': gt_data['markers_in_frame_count']
        }

        return pose

    def detect_markers_simple(self, image):
        """
        Simple marker detection for testing (finds bright spots).
        Replace this with your actual marker detection algorithm.
        """

        # Apply threshold to find bright spots
        _, thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Extract marker centers
        markers_2d = []
        for contour in contours:
            # Calculate centroid
            M = cv2.moments(contour)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                markers_2d.append([cx, cy])

        return np.array(markers_2d, dtype=np.float32) if markers_2d else np.array([]).reshape(0, 2)

    def estimate_pose_pnp(self, markers_2d):
        """
        Estimate camera pose using OpenCV's solvePnP.
        Replace this with your pose estimation algorithm.
        """

        if len(markers_2d) < 4:
            return None, None  # Need at least 4 points for PnP

        # For this simple example, assume we detected markers in order
        # In practice, you would need marker identification/matching
        object_points = self.markers_3D[:len(markers_2d)]
        image_points = markers_2d.reshape(-1, 1, 2)

        # Solve PnP
        success, rvec, tvec = cv2.solvePnP(
            object_points, image_points, 
            self.camera_matrix, self.dist_coeffs
        )

        if success:
            return rvec.flatten(), tvec.flatten()
        else:
            return None, None

    def calculate_pose_error(self, estimated_pose, ground_truth_pose):
        """Calculate pose estimation errors"""

        if estimated_pose[0] is None or estimated_pose[1] is None:
            return {'success': False}

        est_rvec, est_tvec = estimated_pose
        gt_rvec = ground_truth_pose['rotation_vector']
        gt_tvec = ground_truth_pose['translation_vector']

        # Translation error (Euclidean distance in mm)
        translation_error = np.linalg.norm(est_tvec - gt_tvec)

        # Rotation error (angular difference in degrees)
        est_rot = R.from_rotvec(est_rvec)
        gt_rot = R.from_rotvec(gt_rvec)
        relative_rot = est_rot * gt_rot.inv()
        rotation_error = np.degrees(relative_rot.magnitude())

        # Component-wise errors
        component_errors = {
            'tx_error': abs(est_tvec[0] - gt_tvec[0]),
            'ty_error': abs(est_tvec[1] - gt_tvec[1]), 
            'tz_error': abs(est_tvec[2] - gt_tvec[2]),
        }

        return {
            'success': True,
            'translation_error_mm': translation_error,
            'rotation_error_deg': rotation_error,
            **component_errors
        }

    def test_algorithm_on_sample(self, sample_id, detection_func=None, pose_func=None):
        """Test algorithm on a single sample"""

        # Use default functions if none provided
        if detection_func is None:
            detection_func = self.detect_markers_simple
        if pose_func is None:
            pose_func = self.estimate_pose_pnp

        # Load sample
        image, _ = self.load_sample(sample_id)
        ground_truth = self.get_ground_truth_pose(sample_id)

        # Run detection and pose estimation
        markers_2d = detection_func(image)
        estimated_pose = pose_func(markers_2d)

        # Calculate errors
        errors = self.calculate_pose_error(estimated_pose, ground_truth)

        return {
            'sample_id': sample_id,
            'detected_markers': len(markers_2d),
            'ground_truth_markers': ground_truth['markers_visible'],
            **errors
        }

    def evaluate_algorithm(self, sample_subset=None, detection_func=None, pose_func=None):
        """Evaluate algorithm on dataset subset"""

        if sample_subset is None:
            sample_subset = self.df['sample_id'].tolist()

        results = []
        print(f"Testing algorithm on {len(sample_subset)} samples...")

        for i, sample_id in enumerate(sample_subset):
            if i % 50 == 0:
                print(f"  Progress: {i+1}/{len(sample_subset)}")

            result = self.test_algorithm_on_sample(sample_id, detection_func, pose_func)
            results.append(result)

        # Compile statistics
        df_results = pd.DataFrame(results)
        successful_estimates = df_results[df_results['success'] == True]

        if len(successful_estimates) > 0:
            stats = {
                'total_samples': len(results),
                'successful_estimates': len(successful_estimates),
                'success_rate': len(successful_estimates) / len(results),
                'mean_translation_error_mm': successful_estimates['translation_error_mm'].mean(),
                'median_translation_error_mm': successful_estimates['translation_error_mm'].median(),
                'mean_rotation_error_deg': successful_estimates['rotation_error_deg'].mean(),
                'median_rotation_error_deg': successful_estimates['rotation_error_deg'].median(),
                'std_translation_error': successful_estimates['translation_error_mm'].std(),
                'std_rotation_error': successful_estimates['rotation_error_deg'].std()
            }
        else:
            stats = {
                'total_samples': len(results),
                'successful_estimates': 0,
                'success_rate': 0.0
            }

        return df_results, stats

    def create_evaluation_report(self, results_df, stats):
        """Generate a formatted evaluation report"""

        report = "\nPOSE ESTIMATION ALGORITHM EVALUATION REPORT\n"
        report += "=" * 50 + "\n\n"

        report += "Dataset Overview:\n"
        report += f"- Total samples tested: {stats['total_samples']}\n"
        report += f"- Successful pose estimates: {stats['successful_estimates']}\n"
        report += f"- Success rate: {stats['success_rate']:.1%}\n\n"

        if stats['success_rate'] > 0:
            report += "Accuracy Metrics (successful estimates only):\n"
            report += f"- Mean translation error: {stats['mean_translation_error_mm']:.1f} mm\n"
            report += f"- Median translation error: {stats['median_translation_error_mm']:.1f} mm\n"
            report += f"- Std translation error: {stats['std_translation_error']:.1f} mm\n\n"

            report += f"- Mean rotation error: {stats['mean_rotation_error_deg']:.1f} degrees\n"
            report += f"- Median rotation error: {stats['median_rotation_error_deg']:.1f} degrees\n"
            report += f"- Std rotation error: {stats['std_rotation_error']:.1f} degrees\n\n"

            report += "Performance by Marker Visibility:\n"

            # Analyze performance by number of visible markers
            for markers in sorted(results_df['ground_truth_markers'].unique()):
                subset = results_df[results_df['ground_truth_markers'] == markers]
                successful = subset[subset['success'] == True]
                if len(subset) > 0:
                    success_rate = len(successful) / len(subset)
                    report += f"- {markers} markers visible: {len(subset)} samples, {success_rate:.1%} success rate\n"

        return report

# Example usage and testing script
def run_example_evaluation():
    """Example of how to use the evaluation framework"""

    print("EXAMPLE: Testing Simple PnP Algorithm")
    print("=" * 50)

    # Initialize evaluator
    evaluator = PoseEstimationEvaluator("camera_pose_dataset")

    # Test on a subset (samples with good marker visibility)
    good_samples = evaluator.df[evaluator.df['markers_in_frame'] >= 4]['sample_id'].tolist()[:50]

    # Run evaluation
    results_df, stats = evaluator.evaluate_algorithm(sample_subset=good_samples)

    # Generate report
    report = evaluator.create_evaluation_report(results_df, stats)
    print(report)

    # Save results
    results_df.to_csv("algorithm_evaluation_results.csv", index=False)
    print("Detailed results saved to: algorithm_evaluation_results.csv")

if __name__ == "__main__":
    run_example_evaluation()
