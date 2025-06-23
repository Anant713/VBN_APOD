#include "/home/anant/VBN/RPOD-Software/include/vbn/FeatureDetector.hpp"
#include "/home/anant/VBN/RPOD-Software/include/vbn/StaticPoseEstimator.hpp"
#include <fstream>
using std::vector ;
#include <stdio.h>

#include <math.h>

void rotationMatrix(float roll, float pitch, float yaw, float (&R) [3][3]) {
    float cr = cosf(roll);
    float sr = sinf(roll);
    float cp = cosf(pitch);
    float sp = sinf(pitch);
    float cy = cosf(yaw);
    float sy = sinf(yaw);

    R[0][0] = cy * cp;
    R[0][1] = cy * sp * sr - sy * cr;
    R[0][2] = cy * sp * cr + sy * sr;

    R[1][0] = sy * cp;
    R[1][1] = sy * sp * sr + cy * cr;
    R[1][2] = sy * sp * cr - cy * sr;

    R[2][0] = -sp;
    R[2][1] = cp * sr;
    R[2][2] = cp * cr;
}

void eulerToQuaternion(float roll, float pitch, float yaw, std::array<float, 4> (&attitude_quat)) {
    float cy = cosf(yaw * 0.5f);
    float sy = sinf(yaw * 0.5f);
    float cp = cosf(pitch * 0.5f);
    float sp = sinf(pitch * 0.5f);
    float cr = cosf(roll * 0.5f);
    float sr = sinf(roll * 0.5f);

    attitude_quat[0] = cr * cp * cy + sr * sp * sy;  // w
    attitude_quat[1] = sr * cp * cy - cr * sp * sy;  // x
    attitude_quat[2] = cr * sp * cy + sr * cp * sy;  // y
    attitude_quat[3] = cr * cp * sy - sr * sp * cy;  // z
}

int main(){
    FILE* f = fopen("simulated-image.raw","rb");

    uint32_t width = 3280;
    uint32_t height = 2464;

    ImageFrame img;
    img.width = width ;
    img.height = height ;
    img.data.resize(width*height)  ;

    size_t read = fread(img.data.data(),1,width*height,f);
    fclose(f);
    printf("Image read in ImageFrame img\n");
    //crop_from_EKF();

    FeatureFrame features;
    printf("Resized features.points\n");
    //features.frame_id =;
    //features.timestamp_us=;
    int THRESHOLD = 150 ;
    int detected = detect(img , features, THRESHOLD);
    printf("%d\n",detected);
    float Df ,y_m ,z_m ,focal,D1,D2,Az_m , El_m;
    Df = 0.05; // dstance between centre and 4 leds of central 5 led pattern multiplied with focal length
    focal = 0; // focal length
    y_m = 0.2; // Half of image sesnor length in mm in y direction
    z_m = 0.2; // Half of image sesnor length in mm in z direction
    D1 = 0; //Distance of central LED from outers LEDS' 
    D2 = 0; //Distance of central LED from outers LEDS' plane parallel to surface of cubesat
    Az_m = 60*M_PI /180;
    El_m = 45*M_PI /180;
    PoseResult pose ;
    if (detected == 5) five_led(&features,Df, y_m, z_m ,Az_m, El_m, pose);
    else if (detected == 3) three_led(&features,D1, D2 , focal, y_m, z_m ,Az_m , El_m, pose);
    else printf("%d number of leds were detected", detected);
    for(int i=0;i<6;i++){
        printf ("%f ", pose.data[i]);
    }
    float R[3][3] ;
    PoseEstimate pose_data;
    rotationMatrix(pose.data[0],pose.data[1],pose.data[2],R);
    eulerToQuaternion(pose.data[0],pose.data[1],pose.data[2],pose_data.attitude_quat);
        for(int i=0;i<4;i++){
        printf ("\n%f ", pose_data.attitude_quat[i]);
    }
}