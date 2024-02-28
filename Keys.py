import cv2 as cv
import numpy as np
from time import sleep
import keyboard_infr
from keyboard_infr import KeyBoardInterface
if __name__ == '__main__':
    print("hi")
    symb_to_hex = {'w': 0x11, 'a': 0x1E, 's': 0x1F, 'd': 0x20, 'up': 0xC8, 'left': 0xCB, 'right': 0xCD, 'down': 0xD0,
                'enter': 0x1C, 'esc': 0x01, 'two': 0x03, 'z': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30,
                'n': 0x31, 'm': 0x32, 'q': 0x10, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17,
                'o': 0x18, 'p': 0x19, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
                'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'tab': 0x0F}
    k = KeyBoardInterface()
    sleep(2)
    k.pressNrelease(symb_to_hex['w'], 0.1)
    k.pressNrelease(symb_to_hex['a'], 0.1)
    k.pressNrelease(symb_to_hex['s'], 0.1)
    k.pressNrelease(symb_to_hex['d'], 0.1)
    k.pressNrelease(symb_to_hex['up'], 0.1)