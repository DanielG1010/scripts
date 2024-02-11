import os
import argparse
from PIL import Image
from collections import defaultdict

def analyze_images(directory, save_results, per_subdir):
    # Initialize counters
    total_images = 0
    resolution_dict = defaultdict(int)
    format_dict = defaultdict(int)
    mode_dict = defaultdict(int)

    # Initialize variables for smallest and largest resolutions
    smallest_resolution = None
    largest_resolution = None

    # Initialize variable for subdirectories
    subdirs = 0

    # Walk through directory
    for root, dirs, files in os.walk(directory):
        if root != directory:
            subdirs += 1
            if per_subdir:
                # Reset counters for each subdirectory
                total_images = 0
                resolution_dict.clear()
                format_dict.clear()
                mode_dict.clear()
                smallest_resolution = None
                largest_resolution = None

        for file in files:
            # Check if file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                total_images += 1
                try:
                    # Open image and get info
                    with Image.open(os.path.join(root, file)) as img:
                        resolution = img.size
                        img_format = img.format
                        img_mode = img.mode

                        # Update counters
                        resolution_dict[resolution] += 1
                        format_dict[img_format] += 1
                        mode_dict[img_mode] += 1

                        # Update smallest and largest resolutions
                        if smallest_resolution is None or resolution < smallest_resolution:
                            smallest_resolution = resolution
                        if largest_resolution is None or resolution > largest_resolution:
                            largest_resolution = resolution
                except IOError:
                    print(f"Couldn't read {file}. Skipping.")

        if per_subdir and total_images > 0:
            # Print results for each subdirectory
            print_results(root, total_images, resolution_dict, smallest_resolution, largest_resolution, format_dict, mode_dict, save_results)

    if not per_subdir:
        # Print results for the whole directory
        print_results(directory, total_images, resolution_dict, smallest_resolution, largest_resolution, format_dict, mode_dict, save_results)
        print(f"\nNumber of subdirectories analyzed: {subdirs}")

def print_results(directory, total_images, resolution_dict, smallest_resolution, largest_resolution, format_dict, mode_dict, save_results):
    # Prepare output
    output = []
    output.append(f"Directory: {directory}")
    output.append(f"Total number of images: {total_images}")

    # Add resolution info
    output.append("\nResolution info:")
    for resolution, count in resolution_dict.items():
        output.append(f"{resolution}: {count} images ({(count / total_images) * 100:.2f}%)")

    # Add smallest and largest resolutions
    output.append(f"\nSmallest resolution: {smallest_resolution}")
    output.append(f"Largest resolution: {largest_resolution}")

    # Add format info
    output.append("\nFormat info:")
    for img_format, count in format_dict.items():
        output.append(f"{img_format}: {count} images ({(count / total_images) * 100:.2f}%)")

    # Add mode info
    output.append("\nMode info:")
    for img_mode, count in mode_dict.items():
        output.append(f"{img_mode}: {count} images ({(count / total_images) * 100:.2f}%)")

    # Print output
    print("\n".join(output))

    # Save results to a file if requested
    if save_results:
        with open(os.path.join(directory, "image_analysis.txt"), "w") as f:
            f.write("\n".join(output))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze images in a directory.')
    parser.add_argument('directory', type=str, help='The directory to analyze.')
    parser.add_argument('--save', action='store_true', help='Save the results to a file.')
    parser.add_argument('--per_subdir', action='store_true', help='Print results for each subdirectory.')
    args = parser.parse_args()

    analyze_images(args.directory, args.save, args.per_subdir)

