#include "../../include/vbn/FeatureDetector.hpp"
#include <stdlib.h>

int THRESHOLD = 150 ;

// Structure to maintain a contour
typedef struct {
    vector<int> points_x;
    vector<int> points_y;
    double num_points;
} Contour;

FeatureDetector::FeatureDetector(IFeatureExtractor* extractor)
    : extractor_(extractor) {}


// Global variables (minimize these for better practice)

uint8_t* threshold(uint8_t* image,int SIZE){
    uint8_t* binary_img = (uint8_t*)malloc(SIZE * sizeof(uint8_t));
    // if (!binary_img) {
    //     perror("malloc faiFeaturePoint2D");
    //     return NULL;
    // }
    //Converting to binary
    for (size_t i=0 ; i < SIZE; i++) {
        if (image[i] < THRESHOLD){
            binary_img[i] = 0;
        } 
        else binary_img[i]=255;
    }
    return binary_img;

}
void process_image(uint8_t *img_grey, int width, int height,FeatureFrame* leds) {
    // Reset star count
    contour_count = 0;
    int SIZE = width * height ;
    // Allocate memory for thresholded image
    uint8_t *thresh_img = threshold(img_grey,SIZE);
    // if(thresh_img == NULL) {
    //     printf("Memory allocation faiFeaturePoint2D for threshold image\n");
    //     return;
    // }

    // Allocate contours
    std:vector<Contour> contours;
    
    // Find contours in the thresholded image
    int num_contours = find_contours(thresh_img, width, height, contours);
    free(thresh_img);

    for (int i = 0; i < num_contours; i++) { 
        // Calculate moments
        double M[3] = {0}; // M00, M01, M10, M11, M20, M02, etc.
        calculate_moments(&contours[i], M);
        
        if (M[0] > 0) { // M[0] is M00
            // Calculate center of mass
            double cx = M[1] / M[0]; // M10/M00
            double cy = M[2] / M[0]; // M01/M00
  
            // Add to star list
            leds->points.emplace_back(cx - width / 2.0f, cy - height / 2.0f); 
        }
    }
    contours.clear();
    
}
int find_contours(uint8_t *thresh_img, int width, int height,vector<Contour>&contours) {
    int contour_count = 0;
    vector<bool>visited (width * height, false); // Using vector for dynamic size and initialization

    // Direction offsets for 8-connected neighbors
    int dx[8] = {-1, 0, 1, 1, 1, 0, -1, -1};
    int dy[8] = {-1, -1, -1, 0, 1, 1, 1, 0};
    
    // Single scan through the image
    for (int y = 10; y < height - 10; y=y+10) {
        for (int x = 10; x < width - 10; x=x+10) {
            int idx = y * width + x;
            
            // If pixel is white and not visited
            if (thresh_img[idx] == 255 && !visited[idx]) {  // Found a new contour

                // contours[contour_count].allocated_size = CONTOUR_BUFFER_SIZE;
                contours.emplace_back();//as push_back needs an argument to compile

                // Trace the contour using flood fill
                vector<int> stack_x;
                vector<int> stack_y;
                int stack_size = 0;
                
                stack_x.push_back(x);
                stack_y.push_back(y);
                stack_size++;
                
                while (stack_size > 0) {
                    stack_size--;
                    int cx = stack_x[stack_size];
                    int cy = stack_y[stack_size];
                    int cidx = cy * width + cx;
                    
                    if (visited[cidx]) continue;
                    visited[cidx] = 1;
                    
                    // Add to contour if there's space
                    contours[contour_count].points_x.push_back(cx);
                    contours[contour_count].points_y.push_back(cy);
                    contours[contour_count].num_points++;

                    
                    // Check all 8 neighbors
                    for (int d = 0; d < 8; d++) {
                        int nx = cx + dx[d];
                        int ny = cy + dy[d];
                        
                        if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                            int nidx = ny * width + nx;
                            if (thresh_img[nidx] == 255 && !visited[nidx]){
                                stack_x.push_back(nx);
                                stack_y.push_back(ny);
                                stack_size++;
                            }
                        }
                    }
                }
                if(contours[contour_count].num_points <= 3){
                    contours.pop_back(); // Remove small contours
                }
                
                else{
                    contour_count++;
                    if(contours.size()>500) return contour_count ;                   
                }                
                contour_count++;
            }
            
        }
    }
    return contour_count;
}
void calculate_moments(Contour *contour, double *moments) {// Calculate moments for a contour
    // Initialize moments
    for (int i = 0; i < 3; i++) {
        moments[i] = 0.0;
    }
    moments[0] = contour->num_points;
    // Calculate spatial moments
    for (int i = 0; i < contour->num_points; i++) {
        // M10, M01 - first order moments        
        moments[1] += contour->points_x[i];
        moments[2] += contour->points_y[i];
        
    }
}
void extract_leds(FeatureFrame* leds){//If number of detected contours > no.of LEDs, then find combination of blobs with best possible chance of being leds
    
}
bool FeatureDetector::detect(const ImageFrame& img, FeatureFrame& features) {
    // Your core logic here — NO OpenCV, NO hardware specifics
    // Work on input.data, input.width, etc.

    // Only implement if there exists some platform-independent logic 
    // otherwise better to implement in platrform-specific code
    FeatureFrame* leds  = &features;
    uint8_t *img_grey = img.data ;
    process_image(img_grey,img.width,img.height,leds);
    extract_leds(leds);
     /* For example:
        Filtering out low-response keypoints
        Sorting by strength
        Packaging metadata (e.g., timestamp, source ID) */
     
    // return true;
    return extractor_->extract(img, features);
}




