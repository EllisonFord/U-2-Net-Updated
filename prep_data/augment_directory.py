from PIL import Image, ImageOps
import os


def augment_image(image_path, output_directory, file_name):
    # Load the original image
    image = Image.open(image_path)

    # Define the transformations
    transformations = {
        "rotate90": image.rotate(90),
        "rotate180": image.rotate(180),
        "rotate270": image.rotate(270),
        "flip_horizontal": ImageOps.mirror(image),
        "flip_vertical": ImageOps.flip(image),
        # Add more transformations if needed
    }

    # Apply each transformation and save the new image
    for transformation_name, transformed_image in transformations.items():
        # Create a file name for the transformed image
        new_file_name = f"{transformation_name}_{file_name}"
        # Save the transformed image to the output directory
        transformed_image.save(os.path.join(output_directory, new_file_name))


def augment_directory(input_directory, output_directory):
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process all files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')) and not file_name.startswith('.'):
            image_path = os.path.join(input_directory, file_name)
            augment_image(image_path, output_directory, file_name)
            print(f"Augmented images for {file_name} have been saved to {output_directory}")


def main():
    # Set your input and output directories here
    input_directory = 'AllEverFiles3/resized/'
    output_directory = 'AllEverFiles3/augmented/'

    # Run the processing function
    augment_directory(input_directory, output_directory)


main()
