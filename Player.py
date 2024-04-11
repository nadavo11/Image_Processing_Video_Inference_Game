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
        self.previous_mask = None
        self.current_mask = None
        self.center_of_mass = None
        self.height = None
        self.width = None
        self.center_of_upper_mass = None
        self.upper_mask = None
        self.H = 480
        self.W = 640
        self.lean = None
        self.squat = None