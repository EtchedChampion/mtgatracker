import time

import pyautogui

if __name__ == '__main__':
    time.sleep(1)
    for x in range(13):
        time.sleep(.5)
        print(pyautogui.position())
        # pyautogui.moveTo(3700, 950)
        # pyautogui.click(3700, 950)
