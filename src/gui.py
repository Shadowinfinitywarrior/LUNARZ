import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import threading
import subprocess 

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.output_image = None

    def select_image(self, file_path):
        self.original_image = Image.open(file_path)
        self.output_image = self.original_image.copy()
        return self.output_image

    def denoise(self):
        if self.original_image:
            return self.original_image.filter(ImageFilter.MedianFilter(size=3))
        return None

    def histogram_equalization(self):
        if self.original_image:
            return self.original_image.convert("L").point(lambda p: p * 1.5)
        return None

    def gamma_correction(self, gamma):
        if self.original_image:
            lut = [pow(x / 255., gamma) * 255 for x in range(256)]
            return self.original_image.point(lut)
        return None

    def unsharp_mask(self):
        if self.original_image:
            return self.original_image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        return None

    def edge_detection(self):
        if self.original_image:
            return self.original_image.filter(ImageFilter.FIND_EDGES)
        return None

    def save_output_image(self, file_path):
        if self.output_image:
            self.output_image.save(file_path)


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.processor = ImageProcessor()

        self.undo_stack = []
        self.redo_stack = []

        self.bg_color = "#f8f9fa"
        self.primary_color = "#007bff"
        self.success_color = "#28a745"
        self.text_color = "#343a40"
        self.button_font = ("Arial", 11, "bold")
        self.label_font = ("Arial", 14)
        self.title_font = ("Arial", 24, "bold")

        self.root.title("Enhanced Image Processor")
        self.root.geometry("1100x700")
        self.root.configure(bg=self.bg_color)

        # Main Frames:
        self.top_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        self.top_frame.pack(fill="x")

        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Top Frame - Logo and Title:
        self.logo_image = Image.open("logo/logo.png").resize((60, 60))
        self.logo_tk = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self.top_frame, image=self.logo_tk, bg=self.bg_color)
        self.logo_label.pack(side=tk.LEFT, padx=10)

        self.title_label = tk.Label(self.top_frame, text="LUNARZ", font=self.title_font, bg=self.bg_color, fg=self.primary_color)
        self.title_label.pack(side=tk.LEFT, padx=20)

        self.control_frame = tk.Frame(self.root, bg=self.bg_color)
        self.control_frame.pack(side=tk.TOP, fill="x", pady=10)

        button_style = {"bg": self.primary_color, "fg": "white", "padx": 10, "pady": 5, "font": self.button_font}

        # Image Action Buttons aligned horizontally :
        self.select_button = tk.Button(self.control_frame, text="Select Image", command=self.select_image, **button_style)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.denoise_button = tk.Button(self.control_frame, text="Denoise Image", command=self.denoise_image, **button_style)
        self.denoise_button.pack(side=tk.LEFT, padx=5)

        self.histogram_button = tk.Button(self.control_frame, text="Histogram Equalization", command=self.histogram_equalization, **button_style)
        self.histogram_button.pack(side=tk.LEFT, padx=5)

        self.gamma_button = tk.Button(self.control_frame, text="Gamma Correction", command=self.gamma_correction, **button_style)
        self.gamma_button.pack(side=tk.LEFT, padx=5)

        self.sharpen_button = tk.Button(self.control_frame, text="Unsharp Mask", command=self.unsharp_mask, **button_style)
        self.sharpen_button.pack(side=tk.LEFT, padx=5)

        self.edge_detection_button = tk.Button(self.control_frame, text="Edge Detection", command=self.edge_detection, **button_style)
        self.edge_detection_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo, bg="#ffc107", fg="white", padx=10, pady=5, font=self.button_font)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(self.control_frame, text="Redo", command=self.redo, bg="#17a2b8", fg="white", padx=10, pady=5, font=self.button_font)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        self.download_button = tk.Button(self.control_frame, text="Download Image", command=self.download_image, bg=self.success_color, fg="white", padx=10, pady=5, font=self.button_font)
        self.download_button.pack(side=tk.LEFT, padx=10)

        #"Open CNN Image Enhancer" Button
        self.cnn_button = tk.Button(self.control_frame, text="Open CNN Image Enhancer", command=self.run_cnn_script, **button_style)
        self.cnn_button.pack(side=tk.LEFT, padx=5)

        # Input Frame:
        self.input_frame = tk.Frame(self.main_frame, bg=self.bg_color, bd=2, relief=tk.GROOVE)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20)

        self.input_label = tk.Label(self.input_frame, text="Input Image", bg=self.bg_color, fg=self.text_color, font=self.label_font)
        self.input_label.pack(pady=5)

        self.input_canvas_frame = tk.Frame(self.input_frame)
        self.input_canvas_frame.pack()

        self.input_scrollbar_x = tk.Scrollbar(self.input_canvas_frame, orient=tk.HORIZONTAL)
        self.input_scrollbar_y = tk.Scrollbar(self.input_canvas_frame, orient=tk.VERTICAL)

        self.input_canvas = tk.Canvas(self.input_canvas_frame, width=300, height=300, bg='#ffffff',
                                      xscrollcommand=self.input_scrollbar_x.set, yscrollcommand=self.input_scrollbar_y.set)
        self.input_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.input_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_scrollbar_x.config(command=self.input_canvas.xview)
        self.input_scrollbar_y.config(command=self.input_canvas.yview)

        # Output Frame:
        self.output_frame = tk.Frame(self.main_frame, bg=self.bg_color, bd=2, relief=tk.GROOVE)
        self.output_frame.grid(row=0, column=2, padx=20, pady=20)

        self.output_label = tk.Label(self.output_frame, text="Output Image", bg=self.bg_color, fg=self.text_color, font=self.label_font)
        self.output_label.pack(pady=5)

        self.output_canvas_frame = tk.Frame(self.output_frame)
        self.output_canvas_frame.pack()

        self.output_scrollbar_x = tk.Scrollbar(self.output_canvas_frame, orient=tk.HORIZONTAL)
        self.output_scrollbar_y = tk.Scrollbar(self.output_canvas_frame, orient=tk.VERTICAL)

        self.output_canvas = tk.Canvas(self.output_canvas_frame, width=300, height=300, bg='#ffffff',
                                       xscrollcommand=self.output_scrollbar_x.set, yscrollcommand=self.output_scrollbar_y.set)
        self.output_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.output_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_scrollbar_x.config(command=self.output_canvas.xview)
        self.output_scrollbar_y.config(command=self.output_canvas.yview)

        # Manual Filter Buttons : 
        self.filter_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.filter_frame.grid(row=0, column=1, padx=20)

        self.brightness_button = tk.Button(self.filter_frame, text="Adjust Brightness", command=self.adjust_brightness, **button_style)
        self.brightness_button.pack(side=tk.TOP, pady=10)

        self.contrast_button = tk.Button(self.filter_frame, text="Adjust Contrast", command=self.adjust_contrast, **button_style)
        self.contrast_button.pack(side=tk.TOP, pady=10)

        self.sharpness_button = tk.Button(self.filter_frame, text="Adjust Sharpness", command=self.adjust_sharpness, **button_style)
        self.sharpness_button.pack(side=tk.TOP, pady=10)

        self.saturation_button = tk.Button(self.filter_frame, text="Adjust Saturation", command=self.adjust_saturation, **button_style)
        self.saturation_button.pack(side=tk.TOP, pady=10)
        
        self.cnn_button = tk.Button(self.filter_frame, text="Run CNN Enhancer", command=self.run_cnn_enhancer, **button_style)
        self.cnn_button.pack(side=tk.TOP, pady=20) 

    def run_cnn_enhancer(self):
        subprocess.Popen(["python", "cnn.py"])

        self.status_label = tk.Label(self.main_frame, text="Select an image to start", bg=self.bg_color, fg=self.text_color, font=self.label_font)
        self.status_label.grid(row=1, column=0, columnspan=3, pady=20)

    # Image Enhancement Methods:
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")])
        if file_path:
            self.undo_stack.clear()
            self.redo_stack.clear()
            self.output_image = self.processor.select_image(file_path)
            self.undo_stack.append(self.output_image.copy())
            self.show_image(self.output_image, self.input_canvas)
            self.show_image(self.output_image, self.output_canvas)

    def denoise_image(self):
        denoised_image = self.processor.denoise()
        if denoised_image:
            self.update_image(denoised_image)

    def histogram_equalization(self):
        enhanced_image = self.processor.histogram_equalization()
        if enhanced_image:
            self.update_image(enhanced_image)

    def gamma_correction(self):
        gamma = simpledialog.askfloat("Gamma Correction", "Enter Gamma Value (0.1-100):", minvalue=0.1, maxvalue=5.0)
        if gamma:
            gamma_corrected_image = self.processor.gamma_correction(gamma)
            if gamma_corrected_image:
                self.update_image(gamma_corrected_image)

    def unsharp_mask(self):
        sharpened_image = self.processor.unsharp_mask()
        if sharpened_image:
            self.update_image(sharpened_image)

    def edge_detection(self):
        edges_image = self.processor.edge_detection()
        if edges_image:
            self.update_image(edges_image)

    # Adjustment Filters:
    def adjust_brightness(self):
        brightness_value = simpledialog.askfloat("Brightness Adjustment", "Enter Brightness Factor (0.1-10):", minvalue=0.1, maxvalue=2.0)
        if brightness_value:
            enhancer = ImageEnhance.Brightness(self.output_image)
            enhanced_image = enhancer.enhance(brightness_value)
            self.update_image(enhanced_image)

    def adjust_contrast(self):
        contrast_value = simpledialog.askfloat("Contrast Adjustment", "Enter Contrast Factor (0.1-10):", minvalue=0.1, maxvalue=2.0)
        if contrast_value:
            enhancer = ImageEnhance.Contrast(self.output_image)
            enhanced_image = enhancer.enhance(contrast_value)
            self.update_image(enhanced_image)

    def adjust_sharpness(self):
        sharpness_value = simpledialog.askfloat("Sharpness Adjustment", "Enter Sharpness Factor (0.1-10):", minvalue=0.1, maxvalue=2.0)
        if sharpness_value:
            enhancer = ImageEnhance.Sharpness(self.output_image)
            enhanced_image = enhancer.enhance(sharpness_value)
            self.update_image(enhanced_image)

    def adjust_saturation(self):
        saturation_value = simpledialog.askfloat("Saturation Adjustment", "Enter Saturation Factor (0.1-10):", minvalue=0.1, maxvalue=2.0)
        if saturation_value:
            enhancer = ImageEnhance.Color(self.output_image)
            enhanced_image = enhancer.enhance(saturation_value)
            self.update_image(enhanced_image)

    # Helper Methods :
    def update_image(self, new_image):
        self.output_image = new_image
        self.show_image(self.output_image, self.output_canvas)
        self.undo_stack.append(self.output_image.copy())
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.output_image = self.undo_stack[-1]
            self.show_image(self.output_image, self.output_canvas)

    def redo(self):
        if self.redo_stack:
            self.output_image = self.redo_stack.pop()
            self.show_image(self.output_image, self.output_canvas)
            self.undo_stack.append(self.output_image.copy())

    def show_image(self, image, canvas):
        canvas_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas_image)
        canvas.image = canvas_image
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    def download_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("BMP files", "*.bmp")])
        if file_path:
            self.processor.save_output_image(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")

    #CNN Image Enhancer (cnn.py):
    def run_cnn_script(self):
        cnn_script_path = "cnn.py"
        threading.Thread(target=lambda: subprocess.run(["python", cnn_script_path])).start()


root = tk.Tk()
app = ImageApp(root)
root.mainloop()
