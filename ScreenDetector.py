from PIL import ImageGrab, Image
from numpy import array
from directKeys import from_ratio_to_x_y
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def load_image(path):
    image = Image.open(path)
    return image

class ScreenDetector():
    def __init__(self, bbox = None, path=None):
        # Bbox is top left and bottom right coordonates
        # for instance (0, 0, 300, 300)
        if path:
            self.screen = Image.open(path)
        self.screen = ImageGrab.grab(bbox)
        self.screen_arr = array(self.screen)

    def find_pixel(self, r, g, b):
        for i in range(len(self.screen_arr)):
            for j in range(len(self.screen_arr[0])):
                if self.is_pixel_equal(j, i, r, g, b):
                    return j, i
        return -1, -1

    def find_pixel_from_center(self, r, g, b):
        y = int(len(self.screen_arr) / 2)if len(self.screen_arr) % 2 == 1 else int(len(self.screen_arr) / 2) - 1
        x = int(len(self.screen_arr[0]) / 2) if len(self.screen_arr[0]) % 2 == 1 else int(len(self.screen_arr[0]) / 2) - 1
        offset = 1
        
        def droite(x, y, offset, r, g, b):
            if x is None or y is None:
                return None, None, False
            for new_x in range(x + 1, x + offset + 1, 1):
                if new_x == len(self.screen_arr[y]):
                    return None, None, False
                if self.is_pixel_equal(y, new_x, r, g, b):
                    return new_x, y, True
            return new_x, y, False

        def bas(x, y, offset, r, g, b):
            if x is None or y is None:
                return None, None, False
            for new_y in range(y + 1, y + offset + 1, 1):
                if new_y == len(self.screen_arr):
                    return None, None, False
                if self.is_pixel_equal(new_y, x, r, g, b):
                    return x, new_y, True
            return x, new_y, False

        def gauche(x, y, offset, r, g, b):
            if x is None or y is None:
                return None, None, False
            for new_x in range(x - 1, x - offset - 1, -1):
                if new_x == -1:
                    return None, None, False
                if self.is_pixel_equal(y, new_x, r, g, b):
                    return new_x, y, True
            return new_x, y, False

        def haut(x, y, offset, r, g, b):
            if x is None or y is None:
                return None, None, False
            for new_y in range(y - 1, y - offset - 1, -1):
                if new_y == -1:
                    return None, None, False
                if self.is_pixel_equal(new_y, x, r, g, b):
                    return x, new_y, True
            return x, new_y, False

        if self.is_pixel_equal(y, x, r, g, b):
            return x, y, True
        x, y, res = droite(x, y, offset, r, g, b)
        if res == True:
            return x, y, True
        while x is not None and y is not None:
            x, y, res = bas(x, y, offset, r, g, b)
            if res == True:
                return x, y, True
            offset += 1
            x, y, res = gauche(x, y, offset, r, g, b)
            if res == True:
                return x, y, True
            x, y, res = haut(x, y, offset, r, g, b)
            if res == True:
                return x, y, True
            offset += 1
            x, y, res = droite(x, y, offset, r, g, b)
            if res == True:
                return x, y, True
        return x, y, False
        
    def get_text(self):
        return pytesseract.image_to_string(self.screen)

    def get_rgb_value(self, x, y):
        return self.screen_arr[x, y]

    def get_rgb_value_with_ratios(self, ratio_x, ratio_y):
        x, y = from_ratio_to_x_y(ratio_x, ratio_y)
        return self.screen.getpixel((x, y))

    def is_pixel_equal(self, x, y, r, g, b):
        rgb = self.get_rgb_value(x, y)
        r_ = rgb[0]
        g_ = rgb[1]
        b_ = rgb[2]
        return r_ == r and g_ == g and b_ == b

    def is_pixel_equal_with_ratios(self, ratio_x, ratio_y, r, g, b):
        rgb = self.get_rgb_value_with_ratios(ratio_x, ratio_y)
        r_ = rgb[0]
        g_ = rgb[1]
        b_ = rgb[2]
        return r_ == r and g_ == g and b_ == b

    # Asserting sub_image is 2D array of RGB values*
    # x, y are the coordonates of the top left corner in screen
    # of where to look for sub_image
    def is_sub_image_present_within_coordonates(self, sub_image, x, y):
        for i in range(x, x + len(sub_image)):
            for j in range(y, y + len(sub_image[0])):
                if not self.is_pixel_equal(j ,i, sub_image[i - x, j - y, 0], sub_image[i - x, j - y, 1], sub_image[i - x, j - y, 2]):
                    return False
        return True

    # Fucked up, don't use
    def is_sub_image_present(self, sub_image):
        for x in range(self.screen.size[1] - sub_image.shape[1]):
            for y in range(self.screen.size[0] - sub_image.shape[0]):
                if self.is_sub_image_present_within_coordonates(sub_image, x, y):
                    return True
        return False
