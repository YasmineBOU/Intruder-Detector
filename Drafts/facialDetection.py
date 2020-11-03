# import picamera
# import picamera.array
import cv2, os
import numpy as np
from PIL import Image
from scipy.spatial.distance import cosine

#Debug libraries
from pprint import pprint

# Global variables
CAMERA           = None
CASCADE_XML_PATH = "ff.xml"
THRESHOLD        = 0.4


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


def extractROI(inputData="DATABASE/Kay/kay11.jpg"):
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
    # fact    = 1.2;
    # w2, h2  = int(w * fact), int(h * fact)

    # x -= (w2 - w) // 2
    # y -= (h2 - h) // 2

    xf, yf = x + w, y + h


    face_image = Image.fromarray(img[x:xf, y:yf])
    face_image = face_image.resize((224, 224))
    face_array = np.asarray(face_image)
    # face_images.append(face_array)
    
    return face_array
    # return img[y:y + h2, x:x + w2]
    

def get_model_scores(faces):
    
    from keras_vggface.utils import preprocess_input
    from keras_vggface.vggface import VGGFace
    from scipy.spatial.distance import cosine

    samples = np.asarray(faces, 'float32')

    # prepare the data for the model
    samples = preprocess_input(samples, version=2)

    # create a vggface model object
    model = VGGFace(model='resnet50',
      include_top=False,
      input_shape=(224, 224, 3),
      pooling='softmax') # avg

    # perform prediction
    return model.predict(samples)


def loadScores():
    


def getMatching(target):

    folder = "DATABASE"
    subFolderNames = os.listdir(folder)

    scores = []
    filePaths = [target]
    faces = [extractROI(target)]

    finalRes = {}
    ind = 0
    for subFolderName in subFolderNames:
        subFolderPath = os.path.join(
            folder,
            subFolderName
        )

        for filename in os.listdir(subFolderPath):
            filePath = os.path.join(
                subFolderPath,
                filename
            )
            print("{})- '{}'".format(
                ind,
                filePath
            ))

            ind += 1
            filePaths.append(filePath)
            faces.append(extractROI(filePath))

    scores = get_model_scores(faces)

    for ind, score in enumerate(scores[1:]):
        # print("score: {}\nscores: {}\n\n".format(
        #     scores[0],
        #     score
        # ))
        cos = cosine(scores[0], score) 
        if cos <= THRESHOLD:
            print("Faces Matched with  ==> {}".format(

                cos
            ))

            finalRes[ind] = cos

    if finalRes:
        pprint(finalRes)
    else:
        print("Intruder")










if __name__ == "__main__":

    # initVar()
    # output = getImageFromCam()
    # roi    = extractROI(output)
    roi    = extractROI()
    
    if DEBUG:
        # debugAndDisplay(output)
        # debugAndDisplay(roi, "roi.png")
        # debugAndDisplay(roi, "roi.png")
    
        # get_model_scores(roi)
        getMatching(
            # target = "TEST_VALIDATION/face7.jpg"
            # target = "TEST_VALIDATION/knownFaceJenni1.jpg"
            target = "TEST_VALIDATION/dlow7.jpg"
        )