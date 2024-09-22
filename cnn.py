import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, UpSampling2D
setTF_ENABLE_ONEDNN_OPTS=0


def build_denoising_cnn():
    model = Sequential()
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(None, None, 3)))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(3, (3, 3), activation='sigmoid', padding='same'))
    return model


def analyze_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    
    noise_level = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    
    blurriness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    
    contrast = np.std(gray)
    
    return noise_level, blurriness, contrast

class ImageEnhancementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Denoising and Enhancement")

        self.image = None
        self.processed_image = None

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.select_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.select_button.pack()

        self.noise_slider = tk.Scale(master, from_=0, to=100, orient='horizontal', label='Denoising')
        self.noise_slider.pack()
        self.sharpness_slider = tk.Scale(master, from_=0, to=100, orient='horizontal', label='Sharpness')
        self.sharpness_slider.pack()
        self.contrast_slider = tk.Scale(master, from_=0, to=100, orient='horizontal', label='Contrast')
        self.contrast_slider.pack()

        self.update_button = tk.Button(master, text="Update Image", command=self.update_image)
        self.update_button.pack()
        self.save_button = tk.Button(master, text="Save Image", command=self.save_image)
        self.save_button.pack()

    def select_image(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = cv2.imread(filepath)
            self.processed_image = self.image.copy()
            self.show_image(self.image)
            self.analyze_and_suggest(self.image)

    def analyze_and_suggest(self, image):
        noise, blur, contrast = analyze_image(image)
        message = f"Noise Level: {noise:.2f}\nBlurriness: {blur:.2f}\nContrast: {contrast:.2f}"
        messagebox.showinfo("Image Analysis", message)
    
    def update_image(self):
        denoised_image = self.apply_denoising(self.image, self.noise_slider.get())
        sharpened_image = self.apply_sharpening(denoised_image, self.sharpness_slider.get())
        contrasted_image = self.apply_contrast(sharpened_image, self.contrast_slider.get())
        self.processed_image = contrasted_image
        self.show_image(self.processed_image)

    def apply_denoising(self, image, intensity):

        return cv2.fastNlMeansDenoisingColored(image, None, intensity, intensity, 7, 21)

    def apply_sharpening(self, image, intensity):
        kernel = np.array([[0, -1, 0], [-1, 5 + intensity * 0.1, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    def apply_contrast(self, image, intensity):
        alpha = 1.0 + intensity / 100.0 
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=0) 
        return adjusted

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        self.image_label.config(image=image_tk)
        self.image_label.image = image_tk

    def save_image(self):
        if self.processed_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                cv2.imwrite(save_path, self.processed_image)
                messagebox.showinfo("Save Image", f"Image saved at {save_path}")

root = tk.Tk()
app = ImageEnhancementApp(root)
root.mainloop()
