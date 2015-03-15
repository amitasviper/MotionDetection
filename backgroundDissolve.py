import cv2
import numpy as np
import socket

from Queue import Queue
from threading import Thread
from random import randint
import time

class Connection:

	def __init__(self, ip, port, imgQueue):
		self.serverAddress = (ip,port)
		self.workers = 10 			#number of connections to send image to server
		self.myQueue = imgQueue

		#starting all the worker thread(threads will keep on waiting until
		# there is no data to be sent to server)
		self.startWorkers()



	#function that actually send image to server. Executed by each thread parallely
	def sendImage(self,threadNum):

		while True:
			print "%s: Waiting to get images" %threadNum
			frame = self.myQueue.get()		#blocking call... Waits if the myQueue is empty
			self.myQueue.task_done()		#release the lock as soon as it pops data from myQueue

			#encoding image data
			encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
			result, imageEncoded = cv2.imencode('.jpg',frame,encode_param)
			data = np.array(imageEncoded)
			stringData = data.tostring()

			#Perform networking task here
			sock = socket.socket()
			sock.connect(self.serverAddress)
			sock.sendall(stringData)
			sock.close()

			print "Image sent to server"

	#startWorkers() will start all the threads as daemon 
	def startWorkers(self):
		for i in range(self.workers):
			worker = Thread(target=self.sendImage,args=(i,))
			worker.setDaemon(True)
			worker.start()

#locally write the latest image 
def save_frame(frame, outputPath):
	absPath = outputPath + 'pacman.jpg'
	cv2.imwrite(absPath,frame)

#handle the trackbar to change threshold(just for testing purpose)
def changeThreshold(x):
	global pos
	pos = cv2.getTrackbarPos("ThresholdVal","Mask")/100000.0
	print "Trackbar current possition ",pos

if __name__ == "__main__":

	localImagePath = '/opt/lampp/htdocs/opencv/'
	pos = 0.0007	#initial trackbar position

	total = 0

	movingIn = False
	movingOut = False

	prev_contour_count = 0
	curr_contour_count = 0

	curr_area = 0
	prev_area = 0

	settingTime = 20
	startTime = time.time()

	ip = raw_input("Enter server ip: ")
	imageQueue = Queue()   # Queue for holding images to be sent to server
	conn = Connection(ip,5555,imageQueue) #initiating the connection class

	#cv2.namedWindow("Original")
	#cv2.namedWindow("Mask")
	cv2.namedWindow("Motion")
	#cv2.namedWindow("Dilate")
	#cv2.namedWindow("Erode")
	#cv2.namedWindow("Colored Mask")

	bgs = cv2.BackgroundSubtractorMOG2()  #MOG background subtractor(30,1,0.9,0.001)

	cv2.createTrackbar('ThresholdVal','Mask',0,100000,changeThreshold)

	capture = cv2.VideoCapture(0)

	
	while True:

		img = capture.read()[1]
		img = cv2.GaussianBlur(img,(5,5),0)

		tempmask = bgs.apply(img,learningRate=pos)

		thres, fgmask = cv2.threshold(tempmask,20, 255, cv2.THRESH_BINARY)

		#mask_rbg = cv2.cvtColor(fgmask,cv2.COLOR_GRAY2BGR)

		#cv2.imshow("Original",img)
		#cv2.imshow("Mask", fgmask)

		#colored_object = cv2.bitwise_and(img,mask_rbg)

		#cv2.imshow("Colored Mask",colored_object)

		moving_part = cv2.bitwise_and(img,img,mask = fgmask)

		kernel = np.ones((9,9),np.uint8)
		erosion = cv2.erode(fgmask,kernel,iterations=1)

		#cv2.imshow("Erode", erosion)

		dilation = cv2.dilate(erosion,kernel,iterations=1)

		#cv2.imshow("Dilate", dilation)

		contours, hie = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

		if time.time() - startTime < settingTime:
			cv2.drawContours(moving_part,contours,-1,(0,255,0),3)
			cv2.imshow("Motion",moving_part)
			continue

		min_area = 3000
		count = 0
	
		prev_contour_count = curr_contour_count
		curr_contour_count = 0
	
		relevent_contours = []
	
		prev_area = curr_area
		curr_area = 0

		for i in range(len(contours)):

			cnt = contours[i]
			temp_area = cv2.contourArea(cnt)
			
			if temp_area > min_area:
			
				curr_area = temp_area
				approx = cv2.approxPolyDP(cnt,0.001*cv2.arcLength(cnt,True),True)
				relevent_contours.append(approx)
			
				count += 1
				curr_contour_count += 1

		if count != 0:
			if curr_contour_count > prev_contour_count or curr_area - prev_area > 500:
				print "Moving In"
				
				total += 1
				print "Total images added to queue till now: ",total
				imageQueue.put(moving_part) #adding images to queue

				movingIn = True

			cv2.drawContours(moving_part,relevent_contours,-1,(0,255,0),3)

		else:
			curr_contour_count = 0


		if curr_contour_count < prev_contour_count:
			print "Moving Out"
			movingIn = False

		cv2.imshow("Motion",moving_part)
		save_frame(moving_part,localImagePath)
		

		key = cv2.waitKey(30)

		if key >= 27:
			print "Entered into cleanup"
			cv2.destroyAllWindows()
			capture.release()
			break
	print "Main thread in recreation room"
	imageQueue.join()
	print "All Done"