from PIL import ImageGrab, Image
from numpy import array
from directKeys import from_ratio_to_x_y


def load_image(path):
    image = Image.open(path)
    arr = array(image)
    return arr

class ScreenDetector():
    def __init__(self, bbox = None):
        self.screen = ImageGrab.grab(bbox)

    def get_rgb_value(self, x, y):
        return self.screen.getpixel((x, y))

    def get_rgb_value_with_ratios(self, ratio_x, ratio_y):
        x, y = from_ratio_to_x_y(ratio_x, ratio_y)
        return self.screen.getpixel((x, y))

    def is_pixel_equal(self, x, y, r, g, b):
        return self.get_rgb_value(x, y) == (r, g, b)

    def is_pixel_equal_with_ratios(self, ratio_x, ratio_y, r, g, b):
        x, y = from_ratio_to_x_y(ratio_x, ratio_y)
        return self.get_rgb_value(x, y) == (r, g, b)

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
