from directKeys import *
import time

def check_turn():
    #todo
    return True

def play_bullshit_and_die():
    while True:
        if check_turn():
            PressKey("0")
            ReleaseKey("0")
            # click(x, y) # Pos du perso dans timeline
            PressKey(0x11)
            PressKey(0x31)
            ReleaseKey(0x11)
            ReleaseKey(0x31)
            # click(x, y)
            PressKey(0x70)
            ReleaseKey(0x70)
            # spam berserk/mutil/pass
            return

def main():
    # inscription_koli()
    # wait_for_match()
    play_bullshit_and_die()

if __name__ == "__main__":
    # from ScreenDetector import *
    # start = time.process_time()

    # screen = ScreenDetector()
    # image = load_image("test.PNG")
    # print(screen.is_sub_image_present(image))
    # print(time.process_time() - start)

    time.sleep(2)
    main()