#pragma once
#include "../platform/IFeatureExtractor.hpp"
#include "../types/ImageFrame.hpp"
#include "../types/FeatureFrame.hpp"

class FeatureDetector {
public:
    // Constructor with dependency injection
    FeatureDetector(IFeatureExtractor* extractor);

    // Runs feature detection using the underlying extractor
    bool detect(const ImageFrame& img, FeatureFrame& features);

private:
    IFeatureExtractor* extractor_;
};

int detect(ImageFrame& img, FeatureFrame& features, int THRESHOLD, int mode);
void best_comb_five(FeatureFrame* leds);
void best_comb_three(FeatureFrame* leds);
void arrange(FeatureFrame* leds);
void exchange(int idx , int n , FeatureFrame* leds);