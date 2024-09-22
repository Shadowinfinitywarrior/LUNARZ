import cv2
from PIL import Image
import numpy as np

def apply_edge_detection(image_path, method="Canny", lower_thresh=100, upper_thresh=200, apply_blur=False, kernel_size=3):
    """
    Apply edge detection to an image with optional methods (Canny, Sobel, Laplacian).

    Parameters:
    - image_path (str): Path to the image file.
    - method (str): The edge detection method ('Canny', 'Sobel', 'Laplacian').
    - lower_thresh (int): Lower threshold for edge detection (used in Canny).
    - upper_thresh (int): Upper threshold for edge detection (used in Canny).
    - apply_blur (bool): Apply Gaussian blur to the image before edge detection to reduce noise.
    - kernel_size (int): Kernel size for Gaussian blur or Sobel operator (should be odd).

    Returns:
    - PIL.Image: The edge-detected image in PIL format.
    """

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error loading image")
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if apply_blur:
        gray_image = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)
    
    
    if method == "Canny":
        edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
    elif method == "Sobel":
        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size) 
        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size) 
        edges = cv2.magnitude(sobelx, sobely)
        edges = np.uint8(edges)
    elif method == "Laplacian":
        edges = cv2.Laplacian(gray_image, cv2.CV_64F, ksize=kernel_size)
        edges = np.uint8(np.absolute(edges))
    else:
        raise ValueError(f"Unsupported method: {method}. Choose 'Canny', 'Sobel', or 'Laplacian'.")

    return Image.fromarray(edges)

