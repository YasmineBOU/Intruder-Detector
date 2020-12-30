import time
import picamera
from gpiozero import LED, MotionSensor


from IntruderDetector import IntruderDetector


class DetectMovement(object):

	"""docstring for DetectMovement"""


	def __init__(self, args):

		self.ledGPIO = LED(args["ledNum"])
		self.pirGPIO = MotionSensor(args["pirNum"])
		
		self.camera  = picamera.PiCamera() 

		self.ledGPIO.off()

		self.main()
		


	def takeAndSavePicture(self):
		"""
		"""
		# imagePath = time.strftime("%Y-%b-%d_(%H%M%S).png")
		imagePath = time.strftime("personPictured.png")
		self.camera.capture(imagePath)
		return imagePath 



	def main(self):

		while True:

			self.pirGPIO.wait_for_motion()
			print("Motion detected !")
			self.ledGPIO.on()
			imagePath = self.takeAndSavePicture()

			IntruderDetector({
				"imageFilePath" : imagePath
			})

			time.sleep(5)


			self.pirGPIO.wait_for_motion()
			self.ledGPIO.off()
			print("Motion stopped !")




if __name__ == "__main__":

	app = DetectMovement({
		"ledNum" : 17,
		"pirNum" : 4
	})