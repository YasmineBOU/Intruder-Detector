import picamera
import picamera.array
import numpy as np
import cv2

#Debug libraries
from PIL import Image


# Global variables
CAMERA           = None
CASCADE_XML_PATH = "ff.xml"


# Debug variables
DEBUG            = True
IMAGE_FILE_PATHS = [
    "DATABASE/face1.jpg"
]

def initVar():	
    """ Initializes all needed parameters
    """

    global CAMERA 
    CAMERA = picamera.PiCamera() 


def getImageFromCam():
    """
        Returns an array of the captured image
    """

    with picamera.array.PiRGBArray(CAMERA) as output:

        CAMERA.capture(output, 'rgb')
        print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
        return output.array



def debugAndDisplay(inputData, outputData = "TEST.png"):
    """
        Used for debugging blocks of codes

        Args:
            @inputData : the file's path of the targeted image
    """

    PNGFile = Image.fromarray(inputData)
    PNGFile.save(fn)


def extractROI(inputData):
    """
        Returns the locations of the detected region

        Args:
            @inputData : the file's path of the targeted image
    """

    face_cascade = cv2.CascadeClassifier(CASCADE_XML_PATH)
    img          = cv2.imread(inputData)
    gray         = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces        = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print("'{}' : No faces were detected !".format(
            inputData
        ))
        return None


    x, y, w, h  = faces[0]
    # réajuste les coordonnées pour avoir le menton et les cheveux
    fact    = 1.2;
    w2, h2  = (int(w * fact), int(h * fact))

    x -= (w2 - w) // 2
    y -= (h2 - h) // 2
    
    return img[y:y + h2, x:x + w2]
    

if __name__ == "__main__":

    initVar()
    output = getImageFromCam()
    roi    = extractROI(output)
    
    if DEBUG:
        debugAndDisplay(output)
        debugAndDisplay(roi, "roi.png")
        # debugAndDisplay(roi, "roi.png")
