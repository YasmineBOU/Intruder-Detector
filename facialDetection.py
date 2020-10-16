import picamera
import picamera.array
import numpy as np
import cv2

#Debug libraries
from PIL import Image


# Global variables
CAMERA = None
DEBUG = True

def initVar():	
    global CAMERA 
    CAMERA = picamera.PiCamera() 

def getImageFromCam():
    with picamera.array.PiRGBArray(CAMERA) as output:
        CAMERA.capture(output, 'rgb')
        print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
        return output.array

def debugAndDisplay(inputData, fn = "Test.png"):
    PNGFile = Image.fromarray(inputData)
    PNGFile.save(fn)

def extract_roi(inputData):
    face_cascade = cv2.CascadeClassifier('ff.xml')
    img = cv2.imread(inputData)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    x, y, w, h = faces[0]

    # réajuste les coordonnées pour avoir le menton et les cheveux
    fact = 1.2;
    w2, h2 = (int(w * fact), int(h * fact))
    x -= (w2 - w) // 2
    y -= (h2 - h) // 2
    return img[y:y + h2, x:x + w2]
    
if __name__ == "__main__":
    initVar()
    output = getImageFromCam()
    roi = extract_roi(output)
    if DEBUG:
        debugAndDisplay(output)
        debugAndDisplay(roi, "roi.png")
