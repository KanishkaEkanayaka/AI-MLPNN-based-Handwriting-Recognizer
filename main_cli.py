from draw_pad import DrawingCanvas
import matplotlib.pyplot as plt
from preprocess_image import PreprocessImage
from model import Model
import cv2
from voice import SpeakEngine

# initialize speak engine
speak_engine = SpeakEngine()
engine = speak_engine.initiate_engine()
speak_engine.speak(engine, "Welcome to the letter recognition Artificial Intelligence. Please draw the English that that you need to know and then press enter key.")


# create instance of canvas to enable user to draw the drawing
canvas = DrawingCanvas()
canvas.create_window()
draw_img = canvas.run()

preprocessor = PreprocessImage(img=draw_img)
img = preprocessor.preprocessor()
reshaped_img = img.reshape(1,784)

model = Model(img=reshaped_img)
loaded_model = model.load_model()
prediction = model.predictor(loaded_model=loaded_model)
print(str(chr(prediction[0]+96)))
speak_engine.speak(engine, "According to my prediction the letter you draw should be the letter " + str(chr(prediction[0]+96)))
#print(img.shape)

plt.imshow(draw_img)
plt.title('Letter user draw')
plt.show()

plt.imshow(img)
plt.title("Image given to model")
plt.show()
