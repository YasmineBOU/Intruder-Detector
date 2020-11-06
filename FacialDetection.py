import json
import os, sys
import cv2, numpy
from PIL import Image

from keras import backend
from scipy.spatial.distance import cosine
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input


class FacialDetection(object):
	
	"""docstring for FacialDetection"""
	CASCADE_XML_PATH = "ff.xml"
	THRESHOLD        = 0.4
	
	def __init__(self, args):

		self.processDir				  = args["processDir"]
		self.scoreJSONFile 			  = "JSON/scores.json"

		if 'scoreJSONPath' in args:
			self.scoreJSONFile 		  = args["scoreJSONPath"]
		
		if "dataBasePath" in args:
			self.dataBaseFolderPath   = args["dataBasePath"]


		if 'filePath' in args:
			self.fileToProcess		  = args["filePath"]

		self.imageWidth               = 224 #32
		self.imageHeight              = 224 #32
		self.imageDimensions          = (self.imageWidth, self.imageHeight)
		self.nbChannels               = 3

		self.setImageInputShape()
		# self.main()


	def setImageInputShape(self):
		""" 
			Sets the input shape of images
		"""

		if backend.image_data_format() == "channels_first":
			self.imageInputShape = (self.nbChannels, self.imageWidth, self.imageHeight)
			channelsFirst = True
		else:
			self.imageInputShape = (self.imageWidth, self.imageHeight, self.nbChannels)
			self.channelsFirst = False    



	def extractROI(self, imageFilePath):
	    """
	        Returns the locations of the detected region

	        Args:
	            @imageFilePath : the file's path of the targeted image
	    """

	    face_cascade = cv2.CascadeClassifier(self.CASCADE_XML_PATH)
	    img          = cv2.imread(imageFilePath)
	    gray         = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    faces        = face_cascade.detectMultiScale(gray, 1.3, 5)

	    if len(faces) == 0:
	        print("'{}' : No faces were detected !".format(
	            imageFilePath
	        ))
	        return None


	    x, y, w, h  = faces[0]
	    xf, yf 	= x + w, y + h

	    face_image = Image.fromarray(img[x:xf, y:yf])
	    face_image = face_image.resize(self.imageDimensions)
	  	    
	    return numpy.asarray(face_image)


	def getFaceRegions(self):
		"""
			Returns an array of all detected faces from the data set "self.dataBaseFolderPath"

		"""

		filePaths, faces = [], []

		subFolderNames = os.listdir(self.dataBaseFolderPath)

		ind = 0
		for subFolderName in subFolderNames:
			subFolderPath = os.path.join(
				self.dataBaseFolderPath,
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
				faces.append(self.extractROI(filePath))

		return filePaths, faces


	def calculateModelScores(self, faces):
		"""
			Returns an array of scores

			Args:
				@faces: A numpy array of detected faces
		"""

		samples = numpy.asarray(faces, 'float32')

		# prepare the data for the model
		samples = preprocess_input(samples, version=2)

		# create a vggface model object
		model = VGGFace(
			model='resnet50',
			include_top = False,
			input_shape = self.imageInputShape,  
			pooling='softmax' # 'avg'
		) 

		# perform prediction
		return  model.predict(samples)

	    

	def upsertJSONFile(self, newData):
		"""
			Upserts the JSON file of scores and filePaths with new data

			Args:
				@newData : the new data that contains a dict of filePaths and scores:
					newData = {
						"filePaths" : [filePath1, filePath2, ..., filePathN],
						"scores"    : [scoreList1, scoreList2, ..., scoreListN],		
					}  
		"""

		with open(self.scoreJSONFile, "w") as JSONFile:
			json.dump(newScores, JSONFile)


	def loadScoresFromJSONFile(self):
		"""
			Returns the saved data of filePaths and scores 
		"""


		with open(self.scoreJSONFile, "r") as JSONFile:
			return json.load(JSONFile)



	def HaarMethod(self):
		"""
			Depending on if we process a folder of files or just a single file,
			calls the main functions in order to send either:
				-> A dict of filePaths and scores
				-> A list of scores  

		"""

		if self.processDir:

			self.getFaceRegions()
			filePaths, faces = self.getFaceRegions()
			scores = self.calculateModelScores(faces)

			self.upsertJSONFile(
				newData = {
					"filePaths" : filePaths,
					"scores"    : scores.tolist()
				} 
			)

			return None

		else:

			return self.calculateModelScores(
				faces = [self.extractROI(self.fileToProcess)] 
			)



	def main(self, method="Haar"):
		"""
			Main function that calls the appropriated functions 
			depending on the selected method 
		"""newScores

		if method == "Haar":
			return self.HaarMethod()




if __name__ == "__main__":

	args = {
		"dataBasePath" : "DATABASE",
		"scoreJSONPath": "JSON/scores.json",
		"processDir"   : True
	}
newScores

	app = FacialDetection(args)
	app.main()
