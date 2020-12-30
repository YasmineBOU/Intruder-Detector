# import picamera
# import picamera.array
import cv2, os
import numpy as np
from PIL import Image
from scipy.spatial.distance import cosine

from FacialDetection import FacialDetection


from pprint import pprint

''' TF_CPP_MIN_LOG_LEVEL
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
'''
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class IntruderDetector(object):
	
	"""docstring for IntruderDetector"""
	
	# Global variables
	CAMERA           = None
	THRESHOLD        = 0.4


	def __init__(self, args):
		""" 
			Initializes all needed parameters
		"""
		
		self.imageFilePath = args["imageFilePath"]
		# self.CAMERA = picamera.PiCamera() 
		

		self.main()



	def getImageFromCam(self):
		"""
			Returns an array of the captured image
		"""

		with picamera.array.PiRGBArray(self.CAMERA) as output:

			self.CAMERA.capture(output, 'rgb')
			
			print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))

			return output.array



	def main(self):

		app = FacialDetection(
			{
				"processDir" : False,
				"filePath"   : self.imageFilePath
			}
		)

		currentScore = app.main()
		if not currentScore: return
		
		savedData = app.loadScoresFromJSONFile() 
		finalRes  = {}
		# print(savedData.keys())
		for ind, savedScore in enumerate(savedData["scores"]):
			cos = cosine(currentScore, savedScore) 
			if cos <= self.THRESHOLD:
				# print("Faces Matched with {}  ==> {}".format(
				# 	ind, 
				# 	cos
				# ))

				finalRes[ind] = cos

		if not finalRes:

			print("'{}' seems to be an intruder".format(
				self.imageFilePath
			))
			return 0

		filePaths      = savedData['filePaths']		
		distances      = list(finalRes.values())
		minDistance    = min(distances)
		indDict  	   = distances.index(minDistance)
		indMinDistance = list(finalRes.keys())[indDict]


		# print(minDistance, indMinDistance)

		# for ind, filePath in enumerate(filePaths):
		# 	print("{})- {}".format(
		# 		ind,
		# 		filePath
		# 	))


		print("'{}' seems to be '{}'".format(
			self.imageFilePath,
			os.path.dirname(
				filePaths[indMinDistance]
			).split('/')[-1]
		))

		return 1


if __name__ == "__main__":

	TEST_WHOLE_DIR = True

	testDir = "TEST_VALIDATION"

	if TEST_WHOLE_DIR:

		filenames = os.listdir(testDir)
		
		for ind, filename in enumerate(filenames, 1):

			filePath = os.path.join(
				testDir,
				filename
			)

			print('{}/{} - '.format(
				ind,
				len(filenames)
			), end='')

			app = IntruderDetector({

				"imageFilePath" : filePath
			})



	else:

		app = IntruderDetector({
			"imageFilePath" : "TEST_VALIDATION/face1.jpg" #"TEST_VALIDATION/dlow7.jpg"
		})