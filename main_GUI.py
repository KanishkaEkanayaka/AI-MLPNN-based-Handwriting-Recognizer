import tkinter as tk
from tkinter import ttk, Label, Image
from PIL import Image, ImageDraw, ImageGrab, ImageTk  # Added ImageGrab
from preprocess_image import PreprocessImage
from model import Model
import matplotlib.pyplot as plt
import numpy as np
import cv2
from voice import SpeakEngine


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Application")

        # Create four frames
        self.frame1 = ttk.Frame(root)
        self.frame1.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame2 = ttk.Frame(root)
        self.frame2.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame3 = ttk.Frame(root)
        self.frame3.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame4 = ttk.Frame(root)
        self.frame4.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame 1: Canvas for drawing
        self.canvas = tk.Canvas(self.frame1, width=200, height=200, bg="black")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.btn_convert = ttk.Button(self.frame1, text="Predict", command=self.predict_letter)
        self.btn_convert.pack()
        self.btn_clear = ttk.Button(self.frame1, text="Clear", command=self.clear_canvas)
        self.btn_clear.pack()

        # Initialize drawing variables
        self.old_x = None
        self.old_y = None

        # initialize speak engine
        self.speak_engine = SpeakEngine()
        self.engine = self.speak_engine.initiate_engine()

        # Schedule the speak function after a delay
        self.root.after(1000, self.speak_welcome_message)

        # Frame 2: Prediction result
        self.prediction_label = Label(self.frame2, text="Prediction will be displayed here: ", font=("Calibri Bold", 20, "bold"))
        self.prediction_label.pack()

        # Frame 3: Image 1
        self.image_label_1 = Label(self.frame3)
        self.image_label_1.pack()

        # Frame 4: Image 2
        self.image_label_2 = Label(self.frame4)
        self.image_label_2.pack()

    def speak_welcome_message(self):
        self.speak_engine.speak(self.engine, "Welcome to the letter recognition Artificial Intelligence. Please draw the English that that you need to know and then press Predict button.")

    def speak_prediction(self, prediction):
        self.speak_engine.speak(self.engine, "According to my prediction the letter you draw should be the letter " + prediction)


    def draw(self, event):
        x, y = event.x, event.y
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, x, y, fill="white", width=2)
        self.old_x = x
        self.old_y = y

    def clear_canvas(self):
        self.canvas.delete("all")
        self.old_x = None
        self.old_y = None
        self.label.destroy()
    

    def release(self, event):
        self.old_x = None
        self.old_y = None

    def convert_to_image(self):
        # Create an empty image with the same size as the canvas, with a black background
        img = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), color="black")

        # Draw the contents of the canvas onto the image
        draw = ImageDraw.Draw(img)
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if len(coords) > 1:
                draw.line(coords, fill="white", width=2)
        resized_img = cv2.resize(np.array(img), (128, 128))
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        print(resized_img.shape)

        return resized_img
        # Save the image
        # img.save("drawing.png")
        # print("Image saved as drawing.png")
        
    
    def predict_letter(self):
        draw_img = self.convert_to_image()
        preprocessor = PreprocessImage(img=draw_img)
        img = preprocessor.preprocessor()
        reshaped_img = img.reshape(1,784)
    
        model = Model(img=reshaped_img)
        loaded_model = model.load_model()
        prediction = model.predictor(loaded_model=loaded_model)

        # Frame 2: Prediction result
        self.label = Label(self.frame2, text=str(chr(prediction[0]+96)), font=("Calibri Bold", 20, "bold"))
        self.label.pack()
        print(str(chr(prediction[0]+96)))
        self.root.after(1000, lambda: self.speak_prediction(str(chr(prediction[0]+96))))


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = DrawingApp(root)
        root.mainloop()
    except:
        print('error')
    finally:
        speak_engine = SpeakEngine()
        engine = speak_engine.initiate_engine()
        speak_engine.speak(engine, "Thank you and have a nice day!")