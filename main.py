from keyboard_infr import KeyBoardInterface, symb_to_hex
from webcam_stream import WebcamStream
from functions import filter_player, scan_background
import cv2
import numpy as np
import time

# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()

keyboard = KeyBoardInterface()

frame = webcam_stream.read()
H, W = frame.shape[:2]

def get_player_position(mask):
    """
    :param mask: binary mask
    :return: (center_x, center_y)
    """
    # Find indices where we have mass
    mass_x, mass_y = np.where(mask == 255)

    # x,y are the center of x indices and y indices of mass pixels
    center_of_mass = (np.average(mass_x), np.average(mass_y))
    return center_of_mass

def player_lean(player_position, w = W, th = 5):
    # calculate the threshold precentage
    th = w*th//100
    # height
    x = player_position[0]
    # width
    y = player_position[1]

    if y > W//2 + th:
        return 'right'
    if y < W//2 - th:
        return 'left'

def player_control(mask):
    W = mask.shape[1]
    position = get_player_position(mask)

    # lean right and left
    lean = player_lean(position, W)

    if lean == 'left':
        print("left")
        keyboard.pressKey("left")
    else:
        keyboard.releaseKey("left")
    if lean == 'right':
        keyboard.pressKey("right")
    else:
        keyboard.releaseKey("right")

    # add controls here


def play(webcam_stream, background):
    while True:
        # Capture the video frame
        frame = webcam_stream.read()
        # Process the frame
        mask = filter_player(frame, background)
        #grid, mask = process_frame(frame, background)

        # Display the output
        cv2.imshow('output', mask)
        player_control(mask)

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
