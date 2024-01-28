import os
from PIL import Image, UnidentifiedImageError


def resize_image(input_image_path, output_image_path, max_size):
    with Image.open(input_image_path) as img:
        width, height = img.size
        if width > height:
            new_width = max_size
            new_height = int(max_size * height / width)
        else:
            new_height = max_size
            new_width = int(max_size * width / height)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img.save(output_image_path)


def resize_images_in_directory(source_directory, target_directory, max_size=400):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for filename in os.listdir(source_directory):
        # Check for valid image extensions and ignore hidden files or macOS metadata files
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')) and not filename.startswith('.'):
            source_path = os.path.join(source_directory, filename)
            target_path = os.path.join(target_directory, filename)
            try:
                resize_image(source_path, target_path, max_size)
                print(f"Resized image for {filename} has been saved.")
            except UnidentifiedImageError:
                print(f"Cannot identify image file: {source_path}. Skipping.")


# Usage
source_dir = 'AllEverFiles3/'  # Replace with your source directory path
target_dir = 'AllEverFiles3/resized'  # Replace with your target directory path
resize_images_in_directory(source_dir, target_dir)
