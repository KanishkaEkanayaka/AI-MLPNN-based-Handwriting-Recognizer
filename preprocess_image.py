import cv2

class PreprocessImage():

    def __init__(self,img):
        self.img = img

    def preprocessor(self):
        #Apply Gaussian blur filter
        img = cv2.GaussianBlur(self.img, (7,7), 0)

        #Extract the Region of Interest in the image and center in square
        points = cv2.findNonZero(img)
        x, y, w, h = cv2.boundingRect(points)
        if (w > 0 and h > 0):
            if w > h:
                y = y - (w-h)//2
                img = img[y:y+w, x:x+w]
            else:
                x = x - (h-w)//2
                img = img[y:y+h, x:x+h]

        #Resize and resample to be 28 x 28 pixels
        img = cv2.resize(img, (28,28), interpolation = cv2.INTER_CUBIC)

        #Normalize pixels and reshape before adding to the new story array
        img = img/255
        img = img.reshape((28,28))

        return img