#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "tjpgd.h"

static FILE *infile;
static uint8_t *gray_image;

// input callback
static size_t input_func(JDEC *jd, uint8_t *buf, size_t nbyte) {
    if (buf) return fread(buf, 1, nbyte, infile);
    fseek(infile, nbyte, SEEK_CUR);
    return nbyte;
}

// corrected output callback
static int output_func(JDEC *jd, void *bitmap, JRECT *rect) {
    uint8_t *src     = (uint8_t*)bitmap;
    uint16_t rect_w  = rect->right - rect->left + 1;
    uint16_t rect_h  = rect->bottom - rect->top + 1;
    uint16_t img_w   = jd->width;

    for (uint16_t j = 0; j < rect_h; j++) {
        for (uint16_t i = 0; i < rect_w; i++) {
            size_t sidx = (j * rect_w + i) * 3;
            uint8_t r = src[sidx + 0];
            uint8_t g = src[sidx + 1];
            uint8_t b = src[sidx + 2];
            uint8_t gray = (uint8_t)(0.299*r + 0.587*g + 0.114*b);
            uint16_t x = rect->left + i;
            uint16_t y = rect->top  + j;
            gray_image[y * img_w + x] = gray;
        }
    }
    return 1;
}

int main(int argc, char *argv[]) {
    //checking if there are 3 arguments
    if (argc != 3) {
        fprintf(stderr, "Usage: %s in.jpg out.raw\n", argv[0]);
        return 1;
    }
    infile = fopen(argv[1], "rb");
    if (!infile) { perror("fopen in"); return 1; }

    uint8_t workbuf[4096];
    JDEC jd;
    JRESULT res = jd_prepare(&jd, input_func, workbuf, sizeof(workbuf), NULL);
    if (res != JDR_OK) {
        fprintf(stderr, "jd_prepare failed: %d\n", res);
        fclose(infile);
        return 1;
    }

    size_t img_sz = (size_t)jd.width * jd.height;
    gray_image = (uint8_t*)malloc(img_sz);
    if (!gray_image) {
        fprintf(stderr, "malloc %zu bytes failed\n", img_sz);
        fclose(infile);
        return 1;
    }

    printf("Decoding %ux%u…\n", jd.width, jd.height);
    res = jd_decomp(&jd, output_func, 0);
    fclose(infile);
    if (res != JDR_OK) {
        fprintf(stderr, "jd_decomp failed: %d\n", res);
        free(gray_image);
        return 1;
    }

    FILE *out = fopen(argv[2], "wb");
    if (!out) { perror("fopen out"); free(gray_image); return 1; }
    fwrite(gray_image, 1, img_sz, out);
    fclose(out);
    free(gray_image);

    printf("Saved %s (%ux%u raw gray)\n", argv[2], jd.width, jd.height);
    return 0;
}
