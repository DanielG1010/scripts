import os
import argparse
import cv2
import numpy as np
from tqdm import tqdm

# Default directories
default_dirs = ['dir1', 'dir2']

def resize_and_crop_image(input_path, output_path, size):
    image = cv2.imread(input_path)
    h, w = image.shape[:2]

    if h < size[1] or w < size[0]:  # if the image is smaller than the desired size
        image = cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)  # resize (interpolate)
    else:
        # maintain the aspect ratio by cropping
        start_row, start_col = int(h/2-(size[1]/2)), int(w/2-(size[0]/2))
        image = image[start_row:start_row+size[1], start_col:start_col+size[0]]

    cv2.imwrite(output_path, image)

def main():
    parser = argparse.ArgumentParser(description='Resize and crop images.')
    parser.add_argument('--dirs', nargs='*', default=default_dirs, help='Input directories')
    parser.add_argument('--output_dir', required=True, help='Output directory')
    parser.add_argument('--size', nargs=2, type=int, required=True, help='Output resolution')
    args = parser.parse_args()

    size = tuple(map(int, args.size))  # Desired size

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for input_dir in args.dirs:
        parent_dir = os.path.basename(os.path.normpath(input_dir))
        for filename in tqdm(os.listdir(input_dir)):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                output_filename = f"{parent_dir}_{filename}"
                resize_and_crop_image(os.path.join(input_dir, filename), os.path.join(args.output_dir, output_filename), size)

if __name__ == "__main__":
    main()

