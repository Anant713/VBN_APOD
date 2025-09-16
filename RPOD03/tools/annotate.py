import cv2
import sys

def annotate_brightest(image_file, coord_file, n, output_file="annotated.jpg"):
    # Load image
    img = cv2.imread(image_file)
    if img is None:
        raise FileNotFoundError(f"Could not load image {image_file}")

    # Read star coordinates and brightness
    stars = []
    with open(coord_file, "r") as f:
        for line in f:
            if line.strip():
                x, y,b = map(float, line.split(","))
                # shift coords
                x_shifted = int(round(x + 3280/2))
                y_shifted = int(round(y + 2464/2))
                stars.append((x_shifted, y_shifted, b))

                # highlight the pixel in red (BGR order)
                if 0 <= x_shifted < img.shape[1] and 0 <= y_shifted < img.shape[0]:
                    img[y_shifted, x_shifted] = (0, 0, 255)

    # Sort stars by brightness (descending)
    stars.sort(key=lambda s: s[2], reverse=True)

    # Pick top-n brightest
    brightest = stars[:n]
    print("Top stars:", brightest)

    # Annotate brightest stars with circle + label
    for i, (x, y, b) in enumerate(brightest, start=1):
        center = (x, y)
        cv2.circle(img, center, 12, (0, 255, 0), 2)  # green circle
        cv2.putText(img, f"{i}", (center[0] + 15, center[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Save result
    cv2.imwrite(output_file, img)
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     print("Usage: python3 annotate.py <coord_file> [n]")
    #     sys.exit(1)

    path =  f"/home/anant/VBN/RPOD03/blobs.txt"    # coordinate file (e.g., blobs.txt)
    #i = int(sys.argv[2])      # index for image%02d.jpg
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8  # default top 8 stars

    image_file = f"/home/anant/VBN/images/image_23_100um_sun.jpg"       # input name
    #output_file = f"/home/anant/startracking/final_pipeline/resized_images/annotated/anno_image{i:02d}.png" # output name
    output_file = f"/home/anant/VBN/images/annotated.png" # output name


    annotate_brightest(image_file, path, n, output_file)


    #------- DONT FORGET TO UPDATE IMAGE CENTRE ABOVE ------#