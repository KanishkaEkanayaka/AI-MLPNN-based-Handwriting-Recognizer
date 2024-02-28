import cv2
import numpy as np
from tkinter import Tk, Button, Entry, Frame, Label
import keyboard

class DrawingCanvas:
  def __init__(self, canvas_size=128):
    self.canvas_size = canvas_size
    self.window_name = 'Draw Letter'
    self.drawing = False
    self.mode = "idle"
    self.thickness = 2
    self.color = (255, 255, 255)  # Initially white
    self.img = np.zeros((canvas_size, canvas_size), dtype="uint8")
    self.prev_x, self.prev_y = None, None  # Store previous coordinates

  def create_window(self):
    cv2.namedWindow(self.window_name)
    cv2.setMouseCallback(self.window_name, self.mouse_callback)

  def mouse_callback(self, event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
      self.mode = "drawing"
      self.color = (255, 255, 255)  # White strokes
      self.prev_x, self.prev_y = x, y  # Store starting coordinates

    elif event == cv2.EVENT_MOUSEMOVE:
      if self.mode == "drawing" and self.prev_x is not None and self.prev_y is not None:
        # Draw line from previous position to current position
        cv2.line(self.img, (self.prev_x, self.prev_y), (x, y), self.color, self.thickness)
        self.prev_x, self.prev_y = x, y  # Update for next line segment

    elif event == cv2.EVENT_LBUTTONUP:
      self.mode = "idle"
      self.prev_x, self.prev_y = None, None

  def run(self):
    print("Click and drag to draw the letter.")
    print("Press 'q' to quit.")
    print("Press Enter to capture the image.")

    while True:
      cv2.imshow(self.window_name, self.img)
      key = chr(cv2.waitKey(1) & 0xFF)
      
      if keyboard.is_pressed('q'):
        break

      if keyboard.is_pressed('enter'):
        #filename = input("Enter filename (without extension): ") + ".png"
        resized_img = cv2.resize(self.img, (self.canvas_size, self.canvas_size))
        print(resized_img)
        #cv2.imwrite(filename, resized_img)
        #print(f"Image saved as: {filename}")
        return resized_img

if __name__ == "__main__":
    # Example usage
    canvas = DrawingCanvas()
    canvas.create_window()
    canvas.run()
