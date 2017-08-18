# Mirror Keyboard
[![N|Solid](https://secure.gravatar.com/avatar/7273c58dc017eec83667b50742ff6368?s=80)](https://nodesource.com/products/nsolid)

This is a python program which detects motion in a frame using a still camera. It uses python-cv2 to process images. If a motion is detected, then the moving object is extracted from the frame and sent to a server.

The server by default runs on 5555 port and waits for clients to connect. The server can handle multiple connections at a time.

The program learns about the background for about 20 seconds. It has the ablitity to adapt for light changes, or if something gets added to the frame, then it becomes the part of the background after some time. 

### Dependencies:
Install following dependencies via pip: `pip install <module_name>`
	
    1. python2.7
	2. cv2
	3. numpy
	
### Installation
1. Clone the current project to your local machine:
    ```sh
    $ git clone https://github.com/amitasviper/MotionDetection
    ```
2. Run the server on the machine where you want to store the extracted image
    ```
    >> python server.py
    ```
3. Run the client on the machine which is getting the live video feed.
    ```
    >> python backgroundDissolve.py
    ```
