from directKeys import *
from ScreenDetector import *
import time
import random

MOVES = [
    [["1", "2", "3"], ["4"], ["4"], ["4"]], # Sacri
    [["4"], ["5"], ["6"]], # Enu
    [["1"], ["2"], ["3"], ["4"]], # Cra
    [["1"], ["2"], ["3"], ["4"], ["5"]] # Feca
    ]

SUICIDE_T3_WARNING = ["azy gros tue moi", "frere je suicide", "kill me", "bro just kill me ff", "mais fais quelque chose tue moi lance un sort jsp"]

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
    return not screen.is_pixel_equal_with_ratios(0.579167, 0.327778, 39, 39, 34)

def wait_for_match():
    while True:
        time.sleep(4)
        screen = ScreenDetector()
        if screen.is_pixel_equal_with_ratios(0.176042, 0.660185, 194, 233, 1):
            click_with_ratio(0.176042, 0.660185, delay=0.5)
            return

def wait_opponent_double_accept():
    # Wait for the opponent to accept the koli
    while True:
        time.sleep(2)
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

def surrend():
    moveMouseTo_with_ratio(0.7552, 0.93889)
    time.sleep(0.5)
    left_click_without_moving()
    time.sleep(1)
    moveMouseTo_with_ratio(0.441667, 0.536111)
    time.sleep(0.5)
    left_click_without_moving()

def chat_random_stuff():
    click_with_ratio(0.283854, 0.944444)
    time.sleep(1)
    write_whole_str(SUICIDE_T3_WARNING[random.randint(0, len(SUICIDE_T3_WARNING) - 1)] + '\n', delay=0.05)
    time.sleep(0.5)
    moveMouseTo_with_ratio(0.441667, 0.536111)
    time.sleep(0.5)
    left_click_without_moving()

def click_near_pixel(x, y):
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            move_and_left_click(i, j)
            time.sleep(0.25)

def move_near_center():
    screen = ScreenDetector()
    x, y, found = screen.find_pixel_from_center(85, 121, 56)
    if found:
        print("found !")
        click_near_pixel(x, y)
        return
    x, y, found = screen.find_pixel_from_center(90, 125, 62)
    if found:
        click_near_pixel(x, y)
        print("found !")
        return
    else:
        print("Not found...")
        screen.screen.save("pictures\\cell_not_found\\" + time.strftime("%H_%M_%S", time.localtime()) + ".bmp")

def play_bullshit_and_die(index_perso):
    spell_index = 0
    turn_count = 0
    ratio_x, ratio_y = 0.954167, 0.755556 # character in timeline (assuming we don't have ini)
    loaded_moves = MOVES[index_perso]
    while is_fight_going():
        time.sleep(1)
        if is_my_turn():
            time.sleep(0.5)
            move_near_center()
            time.sleep(1)
            turn_count += 1
            moveMouseTo_with_ratio(ratio_x, ratio_y)
            time.sleep(1)
            for move in loaded_moves[spell_index]:
                PressKey_and_click(move, 0.5)
                time.sleep(1.5) # mettre un rnd ici serait pas mal
            click_with_ratio(0.725, 0.897222, delay=1) # Passe tour
            time.sleep(0.5)
            if turn_count == 5:
                surrend()
                break
            if turn_count == 2:
                chat_random_stuff()
            spell_index = turn_count % len(loaded_moves)
    time.sleep(1.5)
    click_with_ratio(0.483333, 0.576852, delay=1)

max_koli = 35

def main():
    i = 0
    while i < max_koli:
        i += 1
        time.sleep(2)
        inscription_koli()
        wait_for_match()
        wait_opponent_double_accept()
        play_bullshit_and_die(0)
        # 0 for sacri | 1 for enu | 2 for cra | 3 for feca



if __name__ == "__main__":
    main()
