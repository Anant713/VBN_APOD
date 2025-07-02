
#!/usr/bin/env python3
"""
Script to generate larger camera pose datasets with custom parameters.
Usage: python generate_large_dataset.py --samples 2000 --method lhs --output large_dataset
"""

import argparse
import sys
sys.path.append('.')  # Add current directory to path

from camera_pose_generator import CameraPoseDatasetGenerator, generate_full_dataset

def main():
    parser = argparse.ArgumentParser(description='Generate large camera pose datasets')
    parser.add_argument('--samples', type=int, default=1000, 
                        help='Number of samples to generate (default: 1000)')
    parser.add_argument('--method', choices=['lhs', 'random', 'grid'], default='lhs',
                        help='Sampling method (default: lhs)')
    parser.add_argument('--output', type=str, default='large_pose_dataset',
                        help='Output directory (default: large_pose_dataset)')
    parser.add_argument('--resolution', type=str, default='3280x2464',
                        help='Image resolution WxH (default: 3280x2464)')

    args = parser.parse_args()

    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
    except:
        print("Error: Resolution must be in format WIDTHxHEIGHT (e.g., 3280x2464)")
        return

    print(f"Generating large dataset:")
    print(f"  Samples: {args.samples}")
    print(f"  Method: {args.method}")
    print(f"  Output: {args.output}")
    print(f"  Resolution: {width}x{height}")
    print()

    # Create generator
    generator = CameraPoseDatasetGenerator(
        output_dir=args.output,
        img_width=width,
        img_height=height
    )

    # Generate dataset
    dataset_summary = generate_full_dataset(
        generator=generator,
        n_samples=args.samples,
        sampling_method=args.method,
        show_progress=True
    )

    print(f"\nLarge dataset generation complete!")
    print(f"Generated {dataset_summary['successful_generations']} samples")
    print(f"Dataset saved to: {args.output}/")

if __name__ == "__main__":
    main()
