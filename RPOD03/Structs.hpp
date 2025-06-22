#pragma once
#include "math.h"
#include <array>
#include <vector>
#include <cstdint>
#include <stdlib.h>
#include <array>


// \brief to hold pose data (6 elements: a, b, c, x, y, z)
struct PoseResult{
    float data[6];
} ;

/// \brief 6-DOF pose estimate output by the RPOD vision system.
struct PoseEstimate {
    // Position in meters (in target or inertial frame depending on convention)
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;

    // Orientation as a quaternion (w, x, y, z)
    std::array<float, 4> attitude_quat = {1.0f, 0.0f, 0.0f, 0.0f};

    // Optional: Pose covariance (diagonal only for embedded constraints)
    std::array<float, 6> covariance_diag = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};

    // Time at which this estimate is valid (microseconds)
    uint64_t timestamp_us = 0;

    // Validity flag (e.g., set false if tracking was lost)
    bool valid = true;
};

struct ImageFrame {
    uint32_t width;
    uint32_t height;
    std::vector<uint8_t> data; // grayscale or RGB
};

/// \brief A 2D feature point (e.g., marker, LED blob, corner).
struct FeaturePoint2D {
    float y;  ///< Pixel x-coordinate
    float z;  ///< Pixel y-coordinate
};

/// \brief Represents a set of detected 2D features in an image.
struct FeatureFrame {
    std::vector<FeaturePoint2D> points; ///< List of 2D points
    uint64_t timestamp_us = 0;          ///< Timestamp in microseconds
    uint32_t frame_id = 0;              ///< Optional sequential frame ID
};
void five_led(FeatureFrame *camframe, float Df, float y_m, float z_m , PoseResult& pose);
void three_led(FeatureFrame *camframe, float Df, float y_m, float z_m , PoseResult& pose);
int detect(const ImageFrame& img, FeatureFrame& features, int THRESHOLD);