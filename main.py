from directKeys import *
from ScreenDetector import *
import time

MOVES = [
    [["1", "2", "3"], ["4"], ["4"], ["4"]], # Sacri
    [["4"], ["5"], ["6"]] # Enu
    ]

def inscription_koli():
    PressKey('k')
    ReleaseKey('k')
    time.sleep(1)
    click_with_ratio(0.640104, 0.562963, delay=0.5)
    time.sleep(1)
    PressKey('k')
    ReleaseKey('k')


def is_my_turn():
    screen = ScreenDetector()
    return screen.is_pixel_equal_with_ratios(0.458854, 0.940741, 252, 200, 0)

def is_fight_going():
    screen = ScreenDetector()
    print(screen.get_rgb_value_with_ratios(0.579167, 0.327778))
    return not screen.is_pixel_equal_with_ratios(0.579167, 0.327778, 39, 39, 34)

def wait_for_match():
    while True:
        time.sleep(5)
        screen = ScreenDetector()
        if screen.is_pixel_equal_with_ratios(0.176042, 0.660185, 194, 233, 1):
            click_with_ratio(0.176042, 0.660185, delay=0.5)
            return

def wait_opponent_double_accept():
    # Wait for the opponent to accept the koli
    while True:
        time.sleep(5)
        screen = ScreenDetector()
        if screen.is_pixel_equal_with_ratios(0.739063, 0.891667, 206, 240, 0):
            click_with_ratio(0.739063, 0.891667, delay=0.5) # We press ready during placement time
            break
        if screen.is_pixel_equal_with_ratios(0.176042, 0.660185, 194, 233, 1): # We accept potential game if previous one was declined by opponent
            click_with_ratio(0.176042, 0.660185, delay=0.5)
    # Wait for the opponent to be ready on the map
    while True:
        time.sleep(1)
        screen = ScreenDetector()
        if(screen.is_pixel_equal_with_ratios(0.919271, 0.774074, 185, 225, 0) or screen.is_pixel_equal_with_ratios(0.95, 0.774074, 191, 230, 0)):
            return
    

def play_bullshit_and_die(index_perso):
    turn_count = 0
    ratio_x, ratio_y = 0.954167, 0.755556 # character in timeline (assuming we don't have ini)
    loaded_moves = MOVES[index_perso]
    while is_fight_going():
        time.sleep(2)
        if is_my_turn():
            moveMouseTo_with_ratio(ratio_x, ratio_y)
            time.sleep(1)
            for move in loaded_moves[turn_count]:
                PressKey_and_click(move, 0.5)
                time.sleep(3) # mettre un rnd ici serait pas mal
            click_with_ratio(0.725, 0.897222, delay=1) # Passe tour
            time.sleep(1)
            turn_count = (turn_count + 1) % len(loaded_moves)
    time.sleep(4)
    click_with_ratio(0.483333, 0.576852, delay=1)


def main():
    while True:
        time.sleep(2)
        inscription_koli()
        wait_for_match()
        wait_opponent_double_accept()
        play_bullshit_and_die(1) # 0 for sacri 1 for enu

if __name__ == "__main__":
    # from ScreenDetector import *
    # start = time.process_time()

    # screen = ScreenDetector()
    # image = load_image("test.PNG")
    # print(screen.is_sub_image_present(image))
    # print(time.process_time() - start)
    main()