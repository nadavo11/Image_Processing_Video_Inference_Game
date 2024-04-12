
from keyboard_interface import KeyboardInterface
from recorder import fake_cam
from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
import trash_functions
import Player_Position
import Frames_Process
from Player import Player
SOURCE = 'webcam'
def play(webcam_stream, background,Mario):
    while True:
        # Capture the video frame
        frame = webcam_stream.read()
        # Process the frame
        #mask = filter_player(frame, background)
        grid, mask = Frames_Process.grid_output(frame, background,Mario)

        # Display the output
        cv2.imshow('output', grid)
        Player_Position.player_control(mask, keyboard, Mario)

        # Handle user input
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('e'):
            # Assuming get_EXPOSURE is a method of webcam_stream that either prints or sets the exposure
            webcam_stream.get_EXPOSURE()


# initializing and starting multi - thread webcam input stream
if SOURCE != 'webcam':
    webcam_stream = fake_cam('./input.avi')
    print("Using fake cam")

else:
    # initializing and starting multi - thread webcam input stream

    webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
    print("Using webcam")
    webcam_stream.start()
keyboard = KeyboardInterface()
Mario = Player()
background = Frames_Process.scan_background(webcam_stream)
play(webcam_stream, background,Mario)
# After the loop release the cap object
webcam_stream.vcap.release()
# Destroy all the windows
cv2.destroyAllWindows()
