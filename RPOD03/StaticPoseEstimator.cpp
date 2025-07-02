//#include "../../include/vbn/FeatureDetector.hpp"
#include <math.h>
#include "Structs.hpp"
#include <fstream>
void three_led(FeatureFrame *camframe, float D1 ,float D2, float f, float y_m, float z_m ,float Az_m,float El_m, PoseResult& pose){
    // Initializing LEDS vectors in target frame with scaling
    // float x_1_nt[3] = { 0.0f, -D1, 0.0f };
    // float x_2_nt[3] = { 0.0f, 0.0f, -D1 };
    // float x_5_nt[3] = { -D2, 0.0f, 0.0f };
    
    // Initializing LEDS vectors in chaser frame with scaling
    float s1 = 1.0f;
    float s2 = 1.0f;
    for (int i=0;i<3;i++){
        printf("x_%d_nc[3]- %f %f \n",i+1,camframe->points[i].y, camframe->points[i].z);
    }
    float x_1_nc[3] = { s1, camframe->points[0].y, camframe->points[0].z };
    float x_2_nc[3] = { s1, camframe->points[1].y, camframe->points[1].z };
    float x_3_nc[3] = { s1, camframe->points[2].y, camframe->points[2].z };
    float x_4_nc[3] = { s1, camframe->points[3].y, camframe->points[3].z };
    float x_5_nc[3] = { s1, camframe->points[4].y, camframe->points[4].z };
    
    // Calculating centre by taking mean
    float xc[3] = { 0.0f, 0.0f, 0.0f };
    
    // Add all vectors
    xc[1] = x_1_nc[1] + x_2_nc[1] + x_3_nc[1] + x_4_nc[1] + x_5_nc[1];
    xc[2] = x_1_nc[2] + x_2_nc[2] + x_3_nc[2] + x_4_nc[2] + x_5_nc[2];

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
    float cos_a = cosf(a);
    float sin_a = sinf(a);
    
    c = asinf((-x_r5[1]*D2 / x_r4[2]*D1) * cos_a) - Az;
    b = asinf((cosf(c + Az) * cos_a) / (sinf(c + Az) * sin_a + (x_r3[1]*D1 / x_r5[2]*D2))) - El;
    
    // float R = (D * f / x_r1[1]) * (cos_a * cosf(c + Az) - sin_a * sinf(c + Az) * sinf(b + El));
    
    float R = ((D1*f)/ x_r1[1]) * (cos_a * cosf(c + Az) - sin_a * sinf(c + Az) * sinf(b + El));
    
    // Create pose result

    pose.data[0] = a;
    pose.data[1] = b;
    pose.data[2] = c;
    pose.data[3] = R * cos_Az * cos_El;
    pose.data[4] = R * sinf(Az) * cos_El;
    pose.data[5] = -R * sinf(El);
    
    return;
}

void five_led(FeatureFrame *camframe, float Df,float focal, float y_m, float z_m ,float tan_Az_m,float tan_El_m, PoseResult& pose) {

    
    // Initializing LEDS vectors in chaser frame with scaling
    float s1 = 1.0f;
    float s2 = 1.0f;
    for (int i=0;i<5;i++){
        printf("x_%d_nc[3]- %f %f \n",i+1,camframe->points[i].y, camframe->points[i].z);
    }
    float x_1_nc[3] = { s1, camframe->points[0].y, camframe->points[0].z };
    float x_2_nc[3] = { s1, camframe->points[1].y, camframe->points[1].z };
    float x_3_nc[3] = { s1, camframe->points[2].y, camframe->points[2].z };
    float x_4_nc[3] = { s1, camframe->points[3].y, camframe->points[3].z };
    float x_5_nc[3] = { s1, camframe->points[4].y, camframe->points[4].z };
 
    // Calculating centre by taking mean
    float xc[3] = { 0.0f, 0.0f, 0.0f };
    
    // Add all vectors
    for(int i = 0; (i < 3); i++) {
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

    for(int i=0;i<3;i++){
        printf("x_r1[%d]= %f ",i,x_r1[i]);
        printf("x_r2[%d]= %f ",i,x_r2[i]);
        printf("x_r3[%d]= %f ",i,x_r3[i]);
        printf("x_r4[%d]= %f ",i,x_r4[i]);
        printf("x_r5[%d]= %f\n",i,x_r5[i]);
    }

    float a = 0.0f, b = 0.0f, c = 0.0f;
    float tan_Az = 0.0f, tan_El = 0.0f, Az = 0.0f, El = 0.0f;
    
    tan_Az = (xc[1] /focal);
    Az = atanf(tan_Az);
    tan_El = -(xc[2] / focal);//cosf(Az)));
    printf("\n tan_Az = %f\n tan_El = %f",tan_Az,tan_El);
    El = atanf(tan_El);
    //printf("Az_m = %f \n El_m =%f \n",Az_m*180/M_PI,El_m*180/M_PI); 
    printf("\nxc[1] = %f \n xc[2] =%f \n",xc[1],xc[2]);  
    printf("Az = %f \n El =%f \n",Az,El);
    float cos_Az = cosf(Az);
    float cos_El = cosf(El);
    float sin_Az = sinf(Az);
    float sin_El = sinf(El);
    
    // Calculate angles using atan2
    a = atan2f(-x_r1[2], x_r2[2]);
    float cos_a = cosf(a);
    float sin_a = sinf(a);
    
    // Calculate c and b (assuming D and f are defined somewhere)
    c = asinf((-x_r5[1] / x_r4[2]) * cos_a) - Az;
    printf("\n sinf(b+El)=%f",(cosf(c + Az) * cos_a) / (sinf(c + Az) * sin_a + (x_r3[1] / x_r5[2])));
    b = asinf((cosf(c + Az) * cos_a) / (sinf(c + Az) * sin_a + (x_r3[1] / x_r5[2]))) - El;
    
    // float R = (D * f / x_r1[1]) * (cos_a * cosf(c + Az) - sin_a * sinf(c + Az) * sinf(b + El));
    float R = (Df / x_r1[1]) * (cos_a * cosf(c + Az) - sin_a * sinf(c + Az) * sinf(b + El));
    
    // Create pose result

    pose.data[0] = a;
    pose.data[1] = b;
    pose.data[2] = c;
    pose.data[3] = Az;
    pose.data[4] = El;
    pose.data[5] = R;
    pose.s_ntnc_nc[0] = R*cos_Az*cos_El;
    pose.s_ntnc_nc[1] = R*sin_Az*cos_El;
    pose.s_ntnc_nc[2] = -R * sin_El;
    
    std::ofstream out("comparison.txt", std::ios::app);  
    if (!out) {
        std::cerr << "Could not open log.txt\n";
    }
    out << "Output "<<pose.data[0]*180/M_PI<<" "<<pose.data[1]*180/M_PI<<" "<<pose.data[2]*180/M_PI<<" "<<pose.s_ntnc_nc[1]<<" "<<pose.s_ntnc_nc[2]<<" "<<pose.s_ntnc_nc[0] <<endl;
    out.close();
    return;
}