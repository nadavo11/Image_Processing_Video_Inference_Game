import ctypes
import time
from threading import Thread, Event ##iris 10/04
from queue import Queue ##iris 10/04

# Accessing the Windows API to send inputs
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions to match those expected by SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),  # Virtual-key code
                ("wScan", ctypes.c_ushort),  # Hardware scan code
                ("dwFlags", ctypes.c_ulong),  # Various flags
                ("time", ctypes.c_ulong),  # Time stamp for the event
                ("dwExtraInfo", PUL)]  # Extra information


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),  # X position
                ("dy", ctypes.c_long),  # Y position
                ("mouseData", ctypes.c_ulong),  # Scroll amount or mouse button pressed
                ("dwFlags", ctypes.c_ulong),  # Action to be taken
                ("time", ctypes.c_ulong),  # Time stamp for the event
                ("dwExtraInfo", PUL)]  # Extra information


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),  # Keyboard input
                ("mi", MouseInput),  # Mouse input
                ("hi", HardwareInput)]  # Hardware input


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),  # Type of input: 0 for mouse, 1 for keyboard
                ("ii", Input_I)]  # Input information


class KeyBoardInterface:
    def __init__(self):
        def __init__(self, hexKeyCode): ##iris 10/04
            self.hexKeyCode = hexKeyCode  # Store hexKeyCode as an instance attribute

            # Setup the thread to call a method that uses self.hexKeyCode
            self.t = Thread(target=self.pressNrelease)  # Note: Don't call the method with ()
            self.t.daemon = True
            self.t.start()
            pass

    def pressKey(self):
        """
        Simulates a key press.
        :param hexKeyCode: Hexadecimal code of the key to press.
        """
        key = symb_to_hex[self.hexKeyCode]

        # Initialize an extra information field. This is often used to specify an additional
        # 32-bit value associated with the keystroke, such as when the keystroke is generated
        # by an input method editor. Here, it's simply set to 0 as we don't need to use it.
        extra = ctypes.c_ulong(0)

        # Create an instance of the Input_I union. This union is capable of holding data for
        # different types of input: keyboard, mouse, or hardware. Since we're simulating a
        # keyboard input, we'll be working with the KeyBdInput structure within this union.
        ii_ = Input_I()

        # Populate the KeyBdInput structure. The arguments are as follows:
        # 0 for the virtual-key code because we're using scan codes,
        # 'key' for the hardware scan code of the key to simulate,
        # 0x0008 to indicate that the scan code is being used,
        # 0 for the time stamp (letting the system provide it),
        # and a pointer to the extra information.
        ii_.ki = KeyBdInput(0, key, 0x0008, 0, ctypes.pointer(extra))

        # Create an Input structure, setting its type to 1 to indicate a keyboard event
        # and passing the Input_I union instance which now contains our keyboard input data.
        x = Input(ctypes.c_ulong(1), ii_)

        # Finally, call the SendInput function with the following parameters:
        # 1 for the number of input structures we're sending,
        # a pointer to our input structure (which contains our keyboard event data),
        # and the size of our input structure. This function call is what simulates the key press.
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def releaseKey(self):
        """
        Simulates a key release.

        :param hexKeyCode: Hexadecimal code of the key to release.
        """
        key = symb_to_hex[self.hexKeyCode]

        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, key, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def set_hexKeyCode(self,hexKeyCode):
        self.hexKeyCode = hexKeyCode
    def pressNrelease(self, delay=0.01):
        """
        Simulates pressing and releasing a key with a delay in between.

        :param hexKeyCode: Hexadecimal code of the key to press and release.
        :param delay: Delay between press and release in seconds.
        """
        #key = symb_to_hex[self.hexKeyCode]

        self.pressKey()
        time.sleep(delay)
        self.releaseKey()


# Mapping of keys to their directX scan codes
# Source: http://www.gamespp.com/directx/directInputKeyboardScanCodes.html


symb_to_hex = {'w': 0x11, 'a': 0x1E, 's': 0x1F, 'd': 0x20, 'up': 0xC8, 'left': 0x1E, 'right': 0x20, 'down': 0xD0,
               'enter': 0x1C, 'esc': 0x01, 'two': 0x03, 'z': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30,
               'n': 0x31, 'm': 0x32, 'q': 0x10, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17,
               'o': 0x18, 'p': 0x19, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
               'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'tab': 0x0F}

"""symb_to_hex = {'w': 0x11, 'a': 0x1E, 's': 0x1F, 'd': 0x20, 'up': 0xC8, 'left': 0xCB, 'right': 0xCD, 'down': 0xD0,
               'enter': 0x1C, 'esc': 0x01, 'two': 0x03, 'z': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30,
               'n': 0x31, 'm': 0x32, 'q': 0x10, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17,
               'o': 0x18, 'p': 0x19, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
               'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'tab': 0x0F}"""
if __name__ == '__main__':
    for i in range(5):
        k = KeyBoardInterface()
        k.pressNrelease(symb_to_hex['w'], 0.1)
        k.pressNrelease(symb_to_hex['a'], 0.1)
        k.pressNrelease(symb_to_hex['s'], 0.1)
        k.pressNrelease(symb_to_hex['d'], 0.1)
        k.pressNrelease(symb_to_hex['up'], 0.1)