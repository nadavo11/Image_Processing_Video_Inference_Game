from keyboard_infr import KeyBoardInterface, symb_to_hex
from webcam_stream import WebcamStream
from functions import filter_player, scan_background
import cv2
import numpy as np

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
        keyboard.pressNrelease(symb_to_hex["left"])
    if lean == 'right':
        keyboard.pressNrelease(symb_to_hex["right"])

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
