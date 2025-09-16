import os
from PIL import Image
import numpy as np

def convert_png(input_dir, output_dir, mode="jpg", quality=95):
    """
    Convert all PNG images in input_dir to RAW or JPG and save in output_dir.
    
    Args:
        input_dir (str): Path to the directory containing PNG files.
        output_dir (str): Path to the directory where converted files will be saved.
        mode (str): "jpg" or "raw" - format to save in.
        quality (int): JPG quality (1–100), default is 95.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".png"):
            png_path = os.path.join(input_dir, file_name)
            base_name = os.path.splitext(file_name)[0]

            with Image.open(png_path) as img:
                rgb_img = img.convert("RGB")  # ensure RGB
                print(rgb_img.size)

                if mode == "jpg":
                    # Save as JPEG
                    out_name = base_name + ".jpg"
                    out_path = os.path.join(output_dir, out_name)
                    rgb_img.save(out_path, "JPEG", quality=quality)
                    print(f"Converted to JPG: {file_name} -> {out_name}")

                elif mode == "raw":
                    # Save as RAW binary (just pixel values)
                    out_name = base_name + ".raw"
                    out_path = os.path.join(output_dir, out_name)
                    arr = np.array(rgb_img, dtype=np.uint8)
                    arr.tofile(out_path)
                    print(f"Converted to RAW: {file_name} -> {out_name}")

                else:
                    print(f"❌ Unknown mode '{mode}'. Use 'jpg' or 'raw'.")
                    return

# Example usage:
# convert_png("/home/anant/startracking/tests/dr_28_cropped", "/home/anant/startracking/output", mode="jpg")
convert_png("/home/anant/VBN/images/angular@42cm", "/home/anant/VBN/images/angular@42cm", mode="raw")
