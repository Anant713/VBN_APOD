//#include "../../include/vbn/FeatureDetector.hpp"
#include "Structs.hpp"
using std::vector ;

// Structure to maintain a contour
typedef struct {
    vector<int> points_x;
    vector<int> points_y;
    int num_points;
} Contour;

// Global variables (minimize these for better practice)

void best_comb_three(FeatureFrame* leds){

}

void best_comb_five(FeatureFrame* leds){

}

void threshold(ImageFrame& img,int SIZE,int THRESHOLD){
    int count=0;
    for (size_t i=0 ; i < SIZE; i++) {
        if (img.data[i] < (THRESHOLD)){
            img.binary[i] = 0;
        } 
        else {
            img.binary[i]=1;
            count++;
        }
    }
    printf("count = %d",count);
}

int find_contours(ImageFrame& img, int width, int height,vector<Contour>&contours) {

    int contour_count = 0;
    vector<bool>visited (width * height, false); // Using vector for dynamic size and initialization

    // Direction offsets for 8-connected neighbors
    int dx[8] = {-1, 0, 1, 1, 1, 0, -1, -1};
    int dy[8] = {-1, -1, -1, 0, 1, 1, 1, 0};
    
    // Single scan through the image
    for (int y = 10; y < height - 11; y=y+10) {
        for (int x = 10; x < width - 11; x=x+10) {
            int idx = y * width + x;
            // If pixel is white and not visited
            if (img.binary[idx] == 1 && !visited[idx]) {  // Found a new contour

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
                            if (img.binary[nidx] == 1 && !visited[nidx]){
                                stack_x.push_back(nx);
                                stack_y.push_back(ny);
                                stack_size++;
                                contours[contour_count].points_x.push_back(nx);
                                contours[contour_count].points_y.push_back(ny);
                                contours[contour_count].num_points++;                                
                            }
                        }
                    }
                }
                if(contours[contour_count].num_points <= 60){
                    printf("waste contour = %d\n",contours[contour_count].num_points );
                    contours.pop_back(); // Remove small contours
                }
                
                else{
                    printf("%d : %d\n",contour_count,contours[contour_count].num_points);
                    contour_count++;
                    //printf("%zu",contours.size());
                    //if(contours.size()>500) return contour_count ;                   
                }                
                //printf("%d",contour_count);
                //fflush(stdout);
            }
            
        }
    }
    
    printf("in find_contours %zu", contours.size());
    //printf("in find_contours %d", contour_count);

    return contour_count;
}

void calculate_moments(Contour *contour, float *moments , ImageFrame& img) {// Calculate moments for a contour
    // Initialize moments
    for (int i = 0; i < 3; i++) {
        moments[i] = 0.0;
    }
    moments[0] = contour->num_points;
    // Calculate spatial moments
    for (int i = 0; i < contour->num_points; i++) {
        // M10, M01 - first order moments   
        float brightness = (img.data[contour->points_y[i]*img.width + contour->points_x[i]])/255.0 ;     
        moments[1] += contour->points_x[i] ;//* brightness;
        moments[2] += contour->points_y[i] ;//* brightness;
        
    }
}

int process_image(ImageFrame& img,FeatureFrame* leds, int THRESHOLD) {
    // Reset star count
    int width = img.width;
    int height = img.height;
    int contour_count = 0;
    int SIZE = width * height ;
    std::vector<Contour> contours;
    ImageFrame thresh_img;
    threshold(img,SIZE, THRESHOLD);
    printf("thresholded , %zu\n",img.data.size());
    fflush(stdout);
    // Find contours in the thresholded image
    int num_contours = find_contours(img, width, height, contours);
    printf("\n%d num_contours\n%zu contours.size()\n",num_contours, contours.size());
    if (num_contours <=2) return num_contours;
    for (int i = 0; i < num_contours; i++) { 
        // Calculate moments
        float M[3] = {0}; // M00, M01, M10, M11, M20, M02, etc.
        calculate_moments(&contours[i], M,img);
        if (M[0] > 0) { // M[0] is M00
            // Calculate center of mass
            double cx = M[1] / M[0]; // M10/M00
            double cy = M[2] / M[0]; // M01/M00
  
            // Add to star list
            //printf("%f %f \n",cx-width/2.0f,cy-height/2.0f);
            //leds->points.emplace_back(cy - height / 2.0f,cx - width / 2.0f);
            leds->points.emplace_back();
            leds->points[i].y = cx - width / 2.0f;
            leds->points[i].z = cy - height / 2.0f;
            
        }
    }
    contours.clear();
    return num_contours;
}

void exchange(int idx , int n , FeatureFrame* leds){
    int tmp ;
    tmp = leds->points[idx].y ;
    leds->points[idx].y =  leds->points[n].y;
    leds->points[n].y = tmp ;
    tmp = leds->points[idx].z ;
    leds->points[idx].z =  leds->points[n].z;
    leds->points[n].z = tmp ;
}

/**
 * Merge any two points in `leds->points` that are closer than `threshold`,
 * replacing each close‑pair with their average.  
 * Operates in O(n²), which is fine for small numbers of LEDs.
 *
 * @param leds        Pointer to your FeatureFrame containing points[]
 * @param threshold   Maximum distance (in pixels) below which two points
 *                    are considered the same.
 */
void mergeCloseLEDs(FeatureFrame* leds, float threshold){
    if (!leds) return;
    const float thresh2 = threshold * threshold;
    const auto& pts = leds->points;
    size_t n = pts.size();
    std::vector<bool> used(n, false);
    std::vector<FeaturePoint2D> merged;
    merged.reserve(n);

    for (size_t i = 0; i < n; ++i) {
        if (used[i]) 
            continue;

        // start a new cluster with pts[i]
        float sumX = pts[i].y;
        float sumY = pts[i].z;
        int   count = 1;
        used[i] = true;

        // find all other points within threshold
        for (size_t j = i + 1; j < n; ++j) {
            if (used[j]) 
                continue;
            float dx = pts[j].y - pts[i].y;
            float dy = pts[j].z - pts[i].z;
            if (dx*dx + dy*dy <= thresh2) {
                sumX += pts[j].y;
                sumY += pts[j].z;
                ++count;
                used[j] = true;
            }
        }

        // average the cluster
        merged.emplace_back(sumX / count, sumY / count);
    }

    // Replace original points with the merged set
    leds->points = std::move(merged);
}


void arrange(FeatureFrame* leds){
    int maxy=0,maxz=1,miny=2,minz =3;
    for(int i=0;i<5;i++){
        if (leds->points[maxy].y < leds->points[i].y) maxy = i;
    }
    exchange (0,maxy,leds);
    for(int i=1;i<5;i++){
        if (leds->points[maxz].z <leds->points[i].z) maxz = i;
    }
    exchange (1,maxz,leds);
    for(int i=2;i<5;i++){
        if (leds->points[miny].y > leds->points[i].y) miny = i;
    }
    exchange (2,miny,leds);  
    for(int i=3;i<5;i++){
        if (leds->points[minz].z > leds->points[i].z) minz = i;
    }
    exchange (3,minz,leds);

}

void extract_leds(FeatureFrame* leds){//If number of detected contours > no.of LEDs, then find combination of blobs with best possible chance of being leds
    mergeCloseLEDs(leds, 6);
    if(leds->points.size()==5){
        arrange(leds); 
        return;}
    else best_comb_five(leds);
    arrange(leds);
}

int detect( ImageFrame& img, FeatureFrame& features, int THRESHOLD) {
    // Your core logic here — NO OpenCV, NO hardware specifics
    // Work on input.data, input.width, etc.
    // Only implement if there exists some platform-independent logic 
    // otherwise better to implement in platrform-specific code
    FeatureFrame* leds  = &features;
    uint8_t *img_grey = img.data.data() ;
    int num_contours = process_image(img,leds,THRESHOLD);
    if (num_contours <= 2) return num_contours;
    for(int i=0;i<leds->points.size();i++){
        printf("%i : x = %f, y = %f\n",i+1,features.points[i].y,features.points[i].z);
    }
    extract_leds(leds);
    printf("\n%zu\n",leds->points.size());
    return leds->points.size();
     /* For example:
        Filtering out low-response keypoints
        Sorting by strength
        Packaging metadata (e.g., timestamp, source ID) */
     
    // return true;
}




