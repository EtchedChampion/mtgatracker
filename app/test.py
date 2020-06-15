import time

import pyautogui

if __name__ == '__main__':
    x_position = 420
    for x in range(13):
        pyautogui.moveTo(x_position, 1050)
        x_position += 85
        # wait till the hover position is parsed
        time.sleep(1)

        if x == 2:
            # we found the card, click and drag into the field
            pyautogui.click(x_position, 1000)
            pyautogui.moveTo(x_position, 600, duration=.4)
            pyautogui.click()
            break
