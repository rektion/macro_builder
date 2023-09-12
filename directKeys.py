import ctypes
import time
import keyboard
from screeninfo import get_monitors

SendInput = ctypes.windll.user32.SendInput

MOUSE_LEFTDOWN = 0x0002     # left button down
MOUSE_LEFTUP = 0x0004       # left button up
MOUSE_RIGHTDOWN = 0x0008    # right button down
MOUSE_RIGHTUP = 0x0010      # right button up
MOUSE_MIDDLEDOWN = 0x0020   # middle button down
MOUSE_MIDDLEUP = 0x0040     # middle button up

# Keyboard Scan Code Mappings
KEYBOARD_MAPPING = {
    'escape': 0x01,
    'esc': 0x01,
    'f1': 0x3B,
    'f2': 0x3C,
    'f3': 0x3D,
    'f4': 0x3E,
    'f5': 0x3F,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'f11': 0x57,
    'f12': 0x58,
    'printscreen': 0xB7,
    'prntscrn': 0xB7,
    'prtsc': 0xB7,
    'prtscr': 0xB7,
    'scrolllock': 0x46,
    'pause': 0xC5,
    '`': 0x29,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    '-': 0x0C,
    '=': 0x0D,
    'backspace': 0x0E,
    'insert': 0xD2 + 1024,
    'home': 0xC7 + 1024,
    'pageup': 0xC9 + 1024,
    'pagedown': 0xD1 + 1024,
    # numpad
    'numlock': 0x45,
    'divide': 0xB5 + 1024,
    'multiply': 0x37,
    'subtract': 0x4A,
    'add': 0x4E,
    'decimal': 0x53,
    'numpadenter': 0x9C + 1024,
    'numpad1': 0x4F,
    'numpad2': 0x50,
    'numpad3': 0x51,
    'numpad4': 0x4B,
    'numpad5': 0x4C,
    'numpad6': 0x4D,
    'numpad7': 0x47,
    'numpad8': 0x48,
    'numpad9': 0x49,
    'numpad0': 0x52,
    # end numpad
    'tab': 0x0F,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '[': 0x1A,
    ']': 0x1B,
    '\\': 0x2B,
    'del': 0xD3 + 1024,
    'delete': 0xD3 + 1024,
    'end': 0xCF + 1024,
    'capslock': 0x3A,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    ';': 0x27,
    "'": 0x28,
    'enter': 0x1C,
    'return': 0x1C,
    'shift': 0x2A,
    'shiftleft': 0x2A,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35,
    'shiftright': 0x36,
    'ctrl': 0x1D,
    'ctrlleft': 0x1D,
    'win': 0xDB + 1024,
    'winleft': 0xDB + 1024,
    'alt': 0x38,
    'altleft': 0x38,
    ' ': 0x39,
    'space': 0x39,
    'altright': 0xB8 + 1024,
    'winright': 0xDC + 1024,
    'apps': 0xDD + 1024,
    'ctrlright': 0x9D + 1024
}

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


from ctypes import windll, Structure, c_long, byref


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def write_whole_str(str, delay=0):
    keyboard.write(str, delay=delay)

def from_ratio_to_x_y(ratio_x, ratio_y):
    monitor = get_monitors()[0]
    return round(monitor.width * ratio_x), round(monitor.height * ratio_y)

# Returns x, y of the current cursor position
def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt
    # return { "x": pt.x, "y": pt.y}/


# Move the cursor to x, y and left click
def move_and_left_click(x, y, delay=0):
    ctypes.windll.user32.SetCursorPos(x, y)
    left_click_without_moving(delay=delay)


def left_click_without_moving(delay=0):
    time.sleep(delay)
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN)  # left down
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP)  # left up


def right_click_without_moving(delay=0):
    time.sleep(delay)
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTDOWN)  # right down
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTUP)  # right up


# Same as click but with ratios instead of pixel position
# Will work on every screen resolution
# click_with_ratio(0.5, 0.5) will click in the middle of the screen
def click_with_ratio(ratio_x, ratio_y, delay=0):
    x, y = from_ratio_to_x_y(ratio_x, ratio_y)
    move_and_left_click(x, y, delay)


# Move cursor to x, y
def moveMouseTo(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)


# Same as moveMouseTo but with ratios instead of pixel position
# Will work on every screen resolution
# moveMouseTo_with_ratio(0.5, 0.5) will put the cursor in the middle of the screen
def moveMouseTo_with_ratio(ratio_x, ratio_y):
    x, y = from_ratio_to_x_y(ratio_x, ratio_y)
    moveMouseTo(x, y)


# Presses the input key
# key_str is of type char
# See KEYBOARD_MAPPING variable for the list of keys
def PressKey(key_str):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, KEYBOARD_MAPPING[key_str], 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# Releases the input key
# key_str is of type char
# See KEYBOARD_MAPPING variable for the list of keys
def ReleaseKey(key_str):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, KEYBOARD_MAPPING[key_str], 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press_multiple_key(key_arr):
    for key in key_arr:
        keyboard.press(key)
        time.sleep(0.15)
    for key in key_arr:
        keyboard.release(key)

# Press a key then click at current location
# Ideal when opening menus and stuff
def PressKey_and_click(key_str, delay_between):
    PressKey(key_str)
    ReleaseKey(key_str)
    time.sleep(delay_between)
    left_click_without_moving()