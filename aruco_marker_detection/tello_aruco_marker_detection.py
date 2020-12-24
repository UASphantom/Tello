# This python script accesses Tello's camera, takes off, and then detects markers to perform certain commands
# In this case we detect marker id 33 and do a forward flip while marker id 1 commands Tello to land
# Modify this script to suit your needs and feel free to open a GitHub issue with any questions

import cv2
import numpy as np
import time
from cv2 import aruco
import socket
import threading

# Command status flag
COMMAND_IN_PROGRESS = False

# Change these to whatever marker ids you prefer
FLIP_MARKER_ID = 33
LAND_MARKER_ID = 1
EMERGENCY_MARKER_ID = 0
FLY_FORWARD_MARKER_ID = 2
TAKE_OFF_MARKER_ID = 3
FLIP_R = 9

# IP and port of Tello
tello_address = ('192.168.10.1', 8889)
# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Let's be explicit and bind to a local port on our machine where Tello can send messages
sock.bind(('', 9000))

# Setup the aruco marker detection
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
aruco_params =  aruco.DetectorParameters_create()

# Function to send a comand to Tello
def send(message):
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

# Function to receive the message from Tello
def receive():
  
  # Make this global so it can be accessed in the thread
  global COMMAND_IN_PROGRESS

  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response, _ = sock.recvfrom(128)
      message = response.decode(encoding='utf-8')
      print("Received message: " + message)

      # If a command was in progress let's reset it to False
      if COMMAND_IN_PROGRESS and "ok" in message:
        print("resetting command in progress")
        COMMAND_IN_PROGRESS = False

    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Initiate tello connection
send("command")

# Delay for 1 second
time.sleep(1)

# Start the camera stream
send("streamon")

# Delay for 1 second
time.sleep(1)

# Get the video stream from Tello on port 11111
camera = cv2.VideoCapture('udp://127.0.0.1:11111')

# This will give the video stream some time to display
time.sleep(3)

# Takeoff 
send("takeoff")

# Loop until program is stopped with q on the keyboard
while(True):
    # Capture frame-by-frame
    ret, frame = camera.read()

    # Convert the color frame to grayscale for marker detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Get marker corners and ids
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    # Loop through the markers (in case more than one is detected)
    for index, id in np.ndenumerate(ids):

      # If we find marker 33 then let's do a front flip
      if not COMMAND_IN_PROGRESS:
        # Do a flip based on aruco marker
        if id == FLIP_MARKER_ID:
          print("Flip marker detected!!!")
          send("flip f")
          COMMAND_IN_PROGRESS = True
        #Do a flip right based on aruco marker
        elif id == FLIP_R:
          print("Flip marker detected!!!")
          send("flip r")
          COMMAND_IN_PROGRESS = True
        # Land based on aruco marker
        elif id == LAND_MARKER_ID:
          print("Land marker detected!!!")
          send("land")
          COMMAND_IN_PROGRESS = True
        # Stop all motors immediately based on aruco marker
        elif id == EMERGENCY_MARKER_ID:
          print("emergency marker detected!!!")
          send("emergency")
          COMMAND_IN_PROGRESS = True
        # fly forward based on aruco marker
        elif id == FLY_FORWARD_MARKER_ID:
          print("Fly Forward marker detected!!!")
          send("forward 100")
          COMMAND_IN_PROGRESS = True
        # Takeoff based on aruco marker
        elif id == TAKE_OFF_MARKER_ID:
          print("Takeoff marker detected!!!")
          send("takeoff")
          COMMAND_IN_PROGRESS = True

    # Display the resulting frame
    cv2.imshow('Tello', markers)

    #time.sleep(.100)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done let's do some cleanup
sock.close()
camera.release()
cv2.destroyAllWindows()