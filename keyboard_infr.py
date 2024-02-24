import ctypes
import time

SendInput = ctypes.windll.user32.SendInput


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
class KeyBoardInterface:
    def __init__(self):
        pass

    def PressKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


    def ReleaseKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                            ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def pressNrelease(self, hexKeyCode, delay = 0.01):
        self.PressKey(hexKeyCode)
        time.sleep(delay)
        self.ReleaseKey(hexKeyCode)

# directx scan codes
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
# https://gist.github.com/tracend/912308

if __name__ == '__main__':
    symb_to_hex = {'w': 0x11, 'a': 0x1E, 's': 0x1F, 'd': 0x20, 'up': 0xC8, 'left': 0xCB, 'right': 0xCD, 'down': 0xD0,
                   'enter': 0x1C, 'esc': 0x01, 'two': 0x03, 'z': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30,
                   'n': 0x31, 'm': 0x32, 'q': 0x10, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17,
                   'o': 0x18, 'p': 0x19, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
                   'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'tab': 0x0F}

    for i in range(5):
        k = KeyBoardInterface()
        k.pressNrelease(symb_to_hex['w'], 0.1)
        k.pressNrelease(symb_to_hex['a'], 0.1)
        k.pressNrelease(symb_to_hex['s'], 0.1)
        k.pressNrelease(symb_to_hex['d'], 0.1)
        k.pressNrelease(symb_to_hex['up'], 0.1)

    
