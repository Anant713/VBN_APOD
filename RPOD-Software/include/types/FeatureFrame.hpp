#pragma once
#include <vector>
#include <cstdint>
#include "iostream" // using to debug , will remove later
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
/// \brief A 2D feature point (e.g., marker, LED blob, corner).
struct FeaturePoint2D {
    float y;  ///< Pixel x-coordinate
    float z;  ///< Pixel y-coordinate
    float size;
    FeaturePoint2D () : y(0.0f) , z(0.0f), size(0.0f) {};
    FeaturePoint2D (float y_coord ,float z_coord) : y(y_coord) , z(z_coord) , size(0.0f) {printf("not default ran");};

};

/// \brief Represents a set of detected 2D features in an image.
struct FeatureFrame {
    std::vector<FeaturePoint2D> points; ///< List of 2D points
    uint64_t timestamp_us = 0;          ///< Timestamp in microseconds
    uint32_t frame_id = 0;              ///< Optional sequential frame ID
};
