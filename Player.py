from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
from scipy import ndimage
from pynput.keyboard import Key, Controller, Listener
import Frames_Process
import Player_Position

class Player:
    def __init__(self):
        self.frame = None
        self.previous_mask = None
        self.current_mask = None
        self.center_of_mass = None
        self.last_center = (0,0)
        self.height = None
        self.width = None
        self.height_of_person = None
        self.squat_th = 8
        self.center_of_upper_mass = None
        self.upper_mask = None
        self.H = 480
        self.W = 640
        self.lean = None
        self.squat = None
        self.jump = None
        self.time_down = time.time()
        self.time_up = time.time()
        self.center_of_center = None

    def set_down(self):
        self.time_down = time.time()

    '''    def set_jump(self,jumping):
        Times = time.time() - self.time_down
        if Times > 3 :
            print("time.time() - self.time_down = ", Times)
            self.jump = jumping
        else:
            print("Times = ", Times)
            self.jump = None'''

