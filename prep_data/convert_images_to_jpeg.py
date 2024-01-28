from PIL import Image
import shutil
import os


def convert_images(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.cr2', '.jpeg', '.jpg', '.tiff')):
            file_path = os.path.join(input_dir, filename)

            # If the file is a JPEG or JPG, copy it directly
            if filename.lower().endswith(('.jpeg', '.jpg')):
                shutil.copy(file_path, output_dir)
            else:
                # Convert CR2 or TIFF to JPEG
                with Image.open(file_path) as img:
                    output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpeg')
                    img.convert('RGB').save(output_file_path, 'jpeg')


input_directory = 'AllEverFiles/MultiFormat'  # Replace with your input directory path
output_directory = 'AllEverFiles/JPEGS'  # Replace with your output directory path

convert_images(input_directory, output_directory)
