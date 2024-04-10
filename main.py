from keyboard_interface import KeyboardInterface
from webcam_stream import WebcamStream
from functions import filter_player, scan_background
import cv2
import numpy as np
from pynput.keyboard import Key, Controller, Listener

# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()

keyboard = KeyboardInterface()

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
        keyboard.press_and_release(Key.left)
    # else:
    #     keyboard.on_release("l")
    if lean == 'right':
        print("right")
        keyboard.press_and_release(Key.right)
    # else:
    #     keyboard.on_release("r")

    # add controls here


def play():
    # setup

    # loop
    while (True):
        # Capture the video frame
        frame = webcam_stream.read()

        # processing stage
        mask = filter_player(frame, background)

        # display
        cv2.imshow('output', mask)
        player_control(mask)

        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            webcam_stream.quit()


background = scan_background(webcam_stream)
play()
# After the loop release the cap object
webcam_stream.vcap.release()
# Destroy all the windows
cv2.destroyAllWindows()
