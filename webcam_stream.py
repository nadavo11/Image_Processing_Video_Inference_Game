import cv2
from settings import *
from threading import Thread

"""______________________________________________________________________________
    *                                                                           *
    *                                                                           *
    *                          camStream setup                                  *
    *                                                                           *
    *___________________________________________________________________________*
"""


class WebcamStream:
    # initialization method
    def __init__(self, stream_id=DEFAULT_CAMERA):
        # default is 0 for main camera
        self.stream_id = stream_id

        # open video capture from the camera id
        self.vcap = cv2.VideoCapture(self.stream_id)

        #  Set exposure value
        self.EXPOSURE_VALUE = self.get_EXPOSURE()
        self.set_EXPOSURE(INITIAL_EXPOSURE_VALUE)

        # Error in opening camera
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)

        # Hardware FPS
        fps_input_stream = int(self.vcap.get(5))
        print("FPS of input stream: {}".format(fps_input_stream))

        # Reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        self.frame_ready = False

        # Error in capturing frame
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)

        # Dont start capturing frames
        self.stopped = True

        # Thread instantiation
        self.t = Thread(target=self.update, args=())

        # Daemon threads run in background for camera
        self.t.daemon = True

    # Start capturing frames using thread
    def start(self):
        self.stopped = False  # Can start capturing frames
        self.t.start()  # Start update Thread to start capturing frames

    # Method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:  # Program Finished
                break
            self.grabbed, self.frame = self.vcap.read()  # Reading frame
            self.frame_ready = True

            # Error in capturing frame
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break

        self.vcap.release()  # Release camera before terminating

    # Return the current captured frame (flipped)
    def read(self):
        return cv2.flip(self.frame, 1)

    # Stop capturing frames from thread
    def stop(self):
        self.stopped = True

    # Exit Program and destroy cv2 objects
    def quit(self):
        self.stopped = True  # Stop capture frames
        self.t.join()  # kill update thread
        self.vcap.release()  # Release camera
        cv2.destroyAllWindows()  # Destroy all the windows
        exit(0)

    # Increase the EXPOSURE VALUE by 1
    def increase_exposure(self):
        self.EXPOSURE_VALUE += 1
        self.vcap.set(cv2.CAP_PROP_EXPOSURE, self.EXPOSURE_VALUE)
        print(f'Exposure Value increased by 1, currently its {self.EXPOSURE_VALUE}\n')

    # Decrease the EXPOSURE VALUE by 1
    def decrease_exposure(self):
        self.EXPOSURE_VALUE -= 1
        self.vcap.set(cv2.CAP_PROP_EXPOSURE, self.EXPOSURE_VALUE)
        print(f'Exposure Value increased by 1, currently its {self.EXPOSURE_VALUE}\n')

    # Get current exposure value of the camera
    def get_EXPOSURE(self):
        # Get the current exposure value
        exposure_value_us = self.vcap.get(cv2.CAP_PROP_EXPOSURE)
        print("Current Exposure Value:", exposure_value_us)
        return exposure_value_us

    # Set Exposure Value of the camera to Exp and disable Auto Exposure
    def set_EXPOSURE(self, Exp):
        self.vcap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.EXPOSURE_VALUE = Exp
        self.vcap.set(cv2.CAP_PROP_EXPOSURE, self.EXPOSURE_VALUE)
        print("Set Current Exposure Value:", Exp)
