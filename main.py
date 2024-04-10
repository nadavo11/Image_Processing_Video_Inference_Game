from keyboard_infr import KeyBoardInterface, symb_to_hex #nadav changed
#from keyboard_interface import KeyboardInterface
from webcam_stream import WebcamStream
from functions import filter_player, scan_background, grid_output,player_control,player_lean,get_player_position
import cv2
import numpy as np
import time
import trash_functions

# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()

keyboard = KeyBoardInterface() # nadav changed
#keyboard = KeyboardInterface()

frame = webcam_stream.read()
H, W = frame.shape[:2]



def play(webcam_stream, background):
    while True:
        # Capture the video frame
        frame = webcam_stream.read()
        # Process the frame
        #mask = filter_player(frame, background)
        grid, mask = grid_output(frame, background)

        # Display the output
        cv2.imshow('output', grid)
        player_control(mask,keyboard)

        # Handle user input
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('e'):
            # Assuming get_EXPOSURE is a method of webcam_stream that either prints or sets the exposure
            webcam_stream.get_EXPOSURE()


background = scan_background(webcam_stream)
play(webcam_stream, background)
# After the loop release the cap object
webcam_stream.vcap.release()
# Destroy all the windows
cv2.destroyAllWindows()
