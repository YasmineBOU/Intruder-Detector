import os, time
import subprocess
import picamera
from gpiozero import LED, MotionSensor


# from IntruderDetector import IntruderDetector


class DetectMovement(object):

	"""docstring for DetectMovement"""


	def __init__(self, args):

		print("-> Initialization part")
		self.ledGPIO = LED(args["ledNum"])
		self.pirGPIO = MotionSensor(args["pirNum"])
		
		# self.camera  = picamera.PiCamera() 

		self.ledGPIO.off()

		self.main()
		


	def takeAndSavePicture(self):
		"""
		"""
		# imagePath = time.strftime("%Y-%b-%d_(%H%M%S).png")
		imagePath = "personPictured.png"
		# self.camera.capture(imagePath)
		return imagePath 



	def main(self):
		print("-> The program started")
		# try:
		# 	print("\t-> Attempt to take a picture")
		# 	self.takeAndSavePicture()

		# finally:
		# 	print("\t-> Close camera")
		# 	self.camera.close()
		
		# return
		
		while True:

			self.pirGPIO.wait_for_motion()
			print("\nMotion detected !")
			self.ledGPIO.on()
			imagePath = self.takeAndSavePicture()

			# IntruderDetector({
			# 	"imageFilePath" : imagePath
			# })

			cmd = "./client"

			subprocess.call(cmd, shell=True)


			time.sleep(5)


			self.pirGPIO.wait_for_motion()
			self.ledGPIO.off()
			print("Motion stopped !")




if __name__ == "__main__":

	app = DetectMovement({
		"ledNum" : 17,
		"pirNum" : 4
	})