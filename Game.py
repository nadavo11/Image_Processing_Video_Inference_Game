import cv2
from webcam_stream import WebcamStream
from keyboard_interface import KeyboardInterface
import Frames_Process
import Player_Position
from settings import *


class Game:
    def __init__(self):
        # Set Camera
        self.cam = WebcamStream(stream_id=DEFAULT_CAMERA)
        self.cam.start()

        # Set Background
        self.background = Frames_Process.scan_background(self.cam)

        # Set Keyboard
        self.keyboard = KeyboardInterface()

    def __del__(self):
        # Release Camera
        self.cam.vcap.release()
        cv2.destroyAllWindows()

    def play(self):
        while True:
            # Capture the video frame
            frame = self.cam.read()

            # Process the frame
            grid, mask = Frames_Process.grid_output(frame, self.background)

            # Display the output
            cv2.imshow('output', grid)
            Player_Position.player_control(mask, self.keyboard)

            # Handle user input
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
