from PIL import Image, UnidentifiedImageError
import numpy as np
import os


# def create_mask(image_path, output_path):
#     try:
#         # Load the image and convert it to RGBA (just in case it's not)
#         image = Image.open(image_path).convert('RGBA')
#         # Convert the image to a numpy array
#         data = np.array(image)
#         # Create a mask where the alpha channel is 0
#         transparency_mask = data[:, :, 3] == 0
#         # Create a new array with just black and white based on transparency
#         mask_data = np.zeros((data.shape[0], data.shape[1], 4), dtype=np.uint8)
#         mask_data[transparency_mask] = [0, 0, 0, 255]  # Black
#         mask_data[~transparency_mask] = [255, 255, 255, 255]  # White
#         # Convert the array back to an image
#         mask_image = Image.fromarray(mask_data, 'RGBA')
#         # Save the mask image
#         mask_image.save(output_path)
#     except UnidentifiedImageError:
#         print(f'Cannot identify image file, skipping: {image_path}')


def create_mask(image_path, output_path):
    try:
        # Load the image and convert it to RGBA (just in case it's not)
        image = Image.open(image_path).convert('RGBA')
        # Convert the image to a numpy array
        data = np.array(image)
        # Create masks based on alpha channel transparency level
        transparent_mask = data[:, :, 3] < 128  # More than 50% transparent
        opaque_mask = data[:, :, 3] >= 128      # 50% or less transparent
        # Create a new array with just black and white based on transparency
        mask_data = np.zeros((data.shape[0], data.shape[1], 4), dtype=np.uint8)
        mask_data[transparent_mask] = [0, 0, 0, 255]   # Black
        mask_data[opaque_mask] = [255, 255, 255, 255]  # White
        # Convert the array back to an image
        mask_image = Image.fromarray(mask_data, 'RGBA')
        # Save the mask image
        mask_image.save(output_path)
    except UnidentifiedImageError:
        print(f'Cannot identify image file, skipping: {image_path}')


def process_directory(input_directory, output_directory):
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process all PNG files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.lower().endswith('.png'):
            input_path = os.path.join(input_directory, file_name)
            output_path = os.path.join(output_directory, file_name)
            create_mask(input_path, output_path)
            print(f'Mask created for {file_name} at {output_path}')


def main():
    # Set your input and output directories here
    image_path = 'AllEverFiles/OUT/'
    output_path = 'AllEverFiles/masks/'

    # Run the processing function
    process_directory(image_path, output_path)


# if __name__ == 'main':
main()
