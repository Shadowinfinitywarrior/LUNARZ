import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from tkinter.simpledialog import askfloat
import tkinter as tk
from tkinter import filedialog

class ImageProcessor:
    def __init__(self):
        self.image = None

    def select_image(self, path=None):
        if path is None:
            root = tk.Tk()
            root.withdraw()  
            path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if path:
            self.image = Image.open(path)
            return self.image
        return None

    def denoise(self):
        if self.image:
            img_cv = np.array(self.image.convert("RGB"))
            denoised = cv2.fastNlMeansDenoisingColored(img_cv, None, 10, 10, 7, 21)
            denoised_img = Image.fromarray(denoised)
            self.image = denoised_img 
            return denoised_img
        return None

    def histogram_equalization(self):
        if self.image:
            img_cv = np.array(self.image.convert("RGB"))
            img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
            hist_eq = cv2.equalizeHist(img_gray)
            hist_eq_img = Image.fromarray(hist_eq)
            self.image = hist_eq_img  
            return hist_eq_img
        return None

    def gamma_correction(self, gamma=None):
        if self.image:
            if gamma is None:
                gamma = askfloat("Gamma Correction", "Enter gamma value:", minvalue=0.1, maxvalue=5.0)
            if gamma:
                img_cv = np.array(self.image.convert("RGB"))
                img_gamma_corrected = np.power(img_cv / 255.0, gamma) * 255
                img_gamma_corrected = np.uint8(img_gamma_corrected)
                gamma_corrected_img = Image.fromarray(img_gamma_corrected)
                self.image = gamma_corrected_img  
                return gamma_corrected_img
        return None

    def unsharp_mask(self):
        if self.image:
            img_cv = np.array(self.image.convert("RGB"))
            blurred = cv2.GaussianBlur(img_cv, (5, 5), 1.0)
            sharpened = cv2.addWeighted(img_cv, 1.5, blurred, -0.5, 0)
            sharpened_img = Image.fromarray(sharpened)
            self.image = sharpened_img  
            return sharpened_img
        return None

    def edge_detection(self):
        if self.image:
            img_cv = np.array(self.image.convert("RGB"))
            img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(img_gray, 100, 200)
            edges_img = Image.fromarray(edges)
            self.image = edges_img  
            return edges_img
        return None

    def gaussian_blur(self):
        if self.image:
            img_cv = np.array(self.image.convert("RGB"))
            blurred = cv2.GaussianBlur(img_cv, (15, 15), 0)
            blurred_img = Image.fromarray(blurred)
            self.image = blurred_img  
            return blurred_img
        return None

    def median_filter(self):
        if self.image:
            img_cv = np.array(self.image.convert("RGB"))
            median_filtered = cv2.medianBlur(img_cv, 15)
            median_filtered_img = Image.fromarray(median_filtered)
            self.image = median_filtered_img 
            return median_filtered_img
        return None

    def adjust_white_balance(self):
        return self.image

    def save_image(self, path):
        if self.image:
            self.image.save(path)

if __name__ == "__main__":
    processor = ImageProcessor()
    processor.select_image() 
