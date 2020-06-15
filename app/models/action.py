from enum import Enum

import pyautogui


class ActionType(Enum):
    BUTTON = 1
    CLICK = 2
    FORCE_REFRESH = 3


class Action:
    def __init__(self, action_type=ActionType.BUTTON, button='space', position=(0, 0)):
        self.action_type: ActionType = action_type
        self.button: str = button
        self.position = position

    def perform(self):
        print(self)
        if self.action_type == ActionType.BUTTON:
            pyautogui.press(self.button)

        if self.action_type == ActionType.CLICK:
            pyautogui.click(self.position[0], self.position[1])

        if self.action_type == ActionType.FORCE_REFRESH:
            pyautogui.moveTo(1046, 1019, duration=0.1)
            pyautogui.moveTo(950, 1000, duration=0.2)
            pyautogui.moveTo(500, 1019, duration=0.1)
            pyautogui.moveTo(380, 1050, duration=0.3)

    def __str__(self):
        if self.action_type == ActionType.BUTTON:
            return 'pressing {}'.format(self.button)

        if self.action_type == ActionType.CLICK:
            print('clicking on location {}'.format(self.position))

        if self.action_type == ActionType.FORCE_REFRESH:
            print('just moving around')
        return 'pressing {}'.format(self.button)
