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
            # slide trought the hand cards
            pyautogui.moveTo(360, 1040, duration=0.1)
            pyautogui.moveTo(800, 1019, duration=0.1)
            pyautogui.moveTo(920, 1050, duration=0.3)
            pyautogui.moveTo(1283, 1002, duration=0.1)
            # move to the middle of the screen
            pyautogui.moveTo(800, 400, duration=0.2)

    def __str__(self):
        if self.action_type == ActionType.BUTTON:
            return 'pressing {}'.format(self.button)

        if self.action_type == ActionType.CLICK:
            return 'clicking on location {}'.format(self.position)

        if self.action_type == ActionType.FORCE_REFRESH:
            return 'just moving around'

        return 'no known action'
