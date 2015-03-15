This is a python program which detects motion in a frame using a still camera. It uses python-cv2 to process images. If a motion is detected, then the moving object is extracted from the frame and sent to a server.

The server by default runs on 5555 port and waits for clients to connect. The server can handle multiple connections at a time.

The program learns about the background for about 20 seconds. It has the ablitity to adapt for light changes, or if something gets added to the frame, then it becomes the part of the background after some time. 

Dependencies:
	python2.7
	python-cv2
	python-numpy
	python-threading

To run the server:
	python server.py

To run the program:
	python backgroundDissolve.py
