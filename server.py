import socket
import threading
import numpy as np
import random
import time
import cv2

def saveImage(imageData):
	data = np.fromstring(imageData,dtype='uint8')
	decodeImage = cv2.imdecode(data,1)
	fileDir = "/home/viper/Documents/opencv/serverImages/"
	fileName = "image-" + "".join(map(str,time.localtime()))+".jpg"
	cv2.imwrite(fileDir+fileName,decodeImage)
	print "Image saved: ", fileName

def handleConnection(clientSocket):
	totalData = []
	data = ""

	while True:
		data = clientSocket.recv(8192)
		if not data:
			break
		totalData.append(data)

	clientSocket.close()
	if len(totalData) != 0:
		saveImage(''.join(totalData))


def startServer(ip,port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((ip,port))
	sock.listen(5)
	print "Server started on: ",port
	while True:
		newSock, address = sock.accept()
		print "Connected to: ",address

		handler = threading.Thread(target=handleConnection,args=(newSock,))
		handler.start()


if __name__ == "__main__":

	startServer("",5555)