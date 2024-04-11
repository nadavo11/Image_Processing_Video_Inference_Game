
from keyboard_interface import KeyboardInterface
from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
import trash_functions
import Player_Position
import Frames_Process

def play(webcam_stream, background):
    while True:
        # Capture the video frame
        frame = webcam_stream.read()
        # Process the frame
        #mask = filter_player(frame, background)
        grid, mask = Frames_Process.grid_output(frame, background)

        # Display the output
        cv2.imshow('output', grid)
        Player_Position.player_control(mask,keyboard)

        # Handle user input
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('e'):
            # Assuming get_EXPOSURE is a method of webcam_stream that either prints or sets the exposure
            webcam_stream.get_EXPOSURE()


# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()
keyboard = KeyboardInterface()
background = Frames_Process.scan_background(webcam_stream)
play(webcam_stream, background)
# After the loop release the cap object
webcam_stream.vcap.release()
# Destroy all the windows
cv2.destroyAllWindows()
