import os
from PIL import Image

def process_batch(image_paths, process_function, output_dir="processed_images", *args, **kwargs):
    """
    Batch processes a list of image files using the specified process function and saves the results.
    
    Parameters:
    - image_paths (list): List of image file paths to process.
    - process_function (function): Function to apply to each image.
    - output_dir (str): Directory where processed images will be saved. Defaults to 'processed_images'.
    - *args, **kwargs: Additional arguments to pass to the process function.
    
    Returns:
    - list: A list of processed image objects.
    """

    os.makedirs(output_dir, exist_ok=True)

    processed_images = []
    for image_path in image_paths:
        try:
            processed_image = process_function(image_path, *args, **kwargs)
            processed_images.append(processed_image)

            image_name = os.path.basename(image_path)
            save_path = os.path.join(output_dir, image_name)
            processed_image.save(save_path)
            print(f"Processed and saved: {save_path}")

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    return processed_images

def load_images_from_directory(directory, extensions=('jpg', 'jpeg', 'png')):
    """
    Load image file paths from a directory.

    Parameters:
    - directory (str): Path to the directory containing images.
    - extensions (tuple): Allowed file extensions. Defaults to ('jpg', 'jpeg', 'png').

    Returns:
    - list: List of image file paths.
    """
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                image_paths.append(os.path.join(root, file))
    return image_paths
