//#include "../../include/vbn/FeatureDetector.hpp"
#include <math.h>
#include "Structs.hpp"

void three_led(FeatureFrame *camframe, float Df, float y_m, float z_m , PoseResult& pose){

}


void five_led(FeatureFrame *camframe, float Df, float y_m, float z_m , PoseResult& pose) {
    // y_m = y_max/tan(Az_max)
    
    // Initializing LEDS vectors in target frame with scaling
    float x_1_nt[3] = { 0.0f, Df, 0.0f };
    float x_2_nt[3] = { 0.0f, 0.0f, Df };
    float x_3_nt[3] = { 0.0f, -Df, 0.0f };
    float x_4_nt[3] = { 0.0f, 0.0f, -Df };
    float x_5_nt[3] = { -Df, 0.0f, 0.0f };
    
    // Initializing LEDS vectors in chaser frame with scaling
    float s1 = 1.0f;
    float s2 = 1.0f;
    float x_1_nc[3] = { s1, camframe->points[0].y, camframe->points[1].z };
    float x_2_nc[3] = { s1, camframe->points[1].y, camframe->points[1].z };
    float x_3_nc[3] = { s1, camframe->points[2].y, camframe->points[1].z };
    float x_4_nc[3] = { s1, camframe->points[3].y, camframe->points[1].z };
    float x_5_nc[3] = { s1, camframe->points[4].y, camframe->points[1].z };
    
    // Calculating centre by taking mean
    float xc[3] = { 0.0f, 0.0f, 0.0f };
    
    // Add all vectors
    for(int i = 0; i < 3; i++) {
        xc[i] = x_1_nc[i] + x_2_nc[i] + x_3_nc[i] + x_4_nc[i];
    }
    
    // Scale by 0.25 (divide by 4 for mean)
    for(int i = 0; i < 3; i++) {
        xc[i] *= 0.25f;
    }
    
    // Calculate relative positions (subtract center)
    float x_r1[3], x_r2[3], x_r3[3], x_r4[3], x_r5[3];
    
    for(int i = 0; i < 3; i++) {
        x_r1[i] = x_1_nc[i] - xc[i];
        x_r2[i] = x_2_nc[i] - xc[i];
        x_r3[i] = x_3_nc[i] - xc[i];
        x_r4[i] = x_4_nc[i] - xc[i];
        x_r5[i] = x_5_nc[i] - xc[i];
    }
    
    float a = 0.0f, b = 0.0f, c = 0.0f;
    float tan_Az = 0.0f, tan_El = 0.0f, Az = 0.0f, El = 0.0f;
    
    tan_Az = (xc[1] / y_m);
    tan_El = (xc[2] / z_m);
    Az = atanf(tan_Az);
    El = atanf(tan_El);
    
    float cos_Az = cosf(Az);
    float cos_El = cosf(El);
    
    // Calculate angles using atan2
    a = atan2f(x_r1[2], x_r2[2]);
    b = atan2f(x_r1[2], x_r2[2]);  // Note: this looks like it should be different from 'a'
    c = atan2f(x_r1[2], x_r2[2]);  // Note: this looks like it should be different from 'a'
    
    float cos_a = cosf(a);
    float sin_a = sinf(a);
    
    // Calculate c and b (assuming D and f are defined somewhere)
    // Note: There seems to be an issue in the original code - using undefined variables
    c = asinf((-x_r5[1] / x_r4[2]) * cos_a) - Az;
    b = asinf((cosf(c + Az) * cos_a) / (sinf(c + Az) * sin_a + (x_r3[1] / x_r5[2]))) - El;
    
    // Calculate R (assuming D and f are defined)
    // Note: Original code references undefined 'D' and 'f' variables
    // float R = (D * f / x_r1[1]) * (cos_a * cosf(c + Az) - sin_a * sinf(c + Az) * sinf(b + El));
    
    float R = (Df / x_r1[1]) * (cos_a * cosf(c + Az) - sin_a * sinf(c + Az) * sinf(b + El));
    
    // Create pose result

    pose.data[0] = a;
    pose.data[1] = b;
    pose.data[2] = c;
    pose.data[3] = R * cos_Az * cos_El;
    pose.data[4] = R * sinf(Az) * cos_El;
    pose.data[5] = -R * sinf(El);
    
    return;
}