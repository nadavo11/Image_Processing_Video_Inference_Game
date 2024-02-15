import os
import cv2
import numpy as np
# from PIL import Image
# from pygame.locals import *
from threading import Thread

"""______________________________________________________________________________
    *                                                                           *
    *                                                                           *
    *                          camStream setup                                  *
    *                                                                           *
    *___________________________________________________________________________*
"""
OPENCV_LOG_LEVEL = 0
WIDTH, HEIGHT = 1080, 1920
GREEN = (0, 255, 0)
RED = (0, 0, 255)


class WebcamStream:
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 1 for main camera

        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))  # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        self.frame_ready = False
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        # thread instantiation
        self.t = Thread(target=self.update, args=())

        self.t.daemon = True  # daemon threads run in background

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            self.frame_ready = True

            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break

        self.vcap.release()

    # method to return latest read frame
    def read(self):
        return cv2.flip(self.frame, 1)

    # method to stop reading frames
    def stop(self):
        self.stopped = True
    def quit(self):
        self.stopped = True
        self.t.join()
        # After the loop release the cap object
        self.vcap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        exit(0)

    # method to play the game with the user's update function

