#pragma once
#include <array>
#include <cstdint>
#include "/home/anant/VBN/RPOD-Software/include/types/FeatureFrame.hpp"
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

// \brief to hold pose data (6 elements: a, b, c, x, y, z)
struct PoseResult{
    float data[6];
    float s_ntnc_nc[3] ;
} ;
void five_led(FeatureFrame *camframe, float Df,float focal, float y_m, float z_m ,float Az_m,float El_m, PoseResult& pose);
void three_led(FeatureFrame *camframe, float D1 ,float D2, float focal, float y_m, float z_m ,float Az_m,float El_m, PoseResult& pose);
