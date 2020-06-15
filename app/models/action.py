import time
from enum import Enum

import pyautogui

from app.models.card import GameCard
from app.mtga_app import mtga_watch_app


class ActionType(Enum):
    BUTTON = 1
    CLICK = 2
    FORCE_REFRESH = 3
    PLAY = 4


class Action:
    def __init__(self, action_type=ActionType.BUTTON, button='space', position=(0, 0), card=None):
        self.action_type: ActionType = action_type
        self.button: str = button
        self.position = position
        self.card: GameCard = card

    def perform(self):
        print(self)
        game = mtga_watch_app.game
        if self.action_type == ActionType.BUTTON:
            pyautogui.press(self.button)

        elif self.action_type == ActionType.CLICK:
            pyautogui.click(self.position[0], self.position[1])

        elif self.action_type == ActionType.FORCE_REFRESH:
            # slide trough the hand cards
            pyautogui.moveTo(360, 1040, duration=0.1)
            pyautogui.moveTo(800, 1019, duration=0.1)
            pyautogui.moveTo(920, 1050, duration=0.3)
            pyautogui.moveTo(1283, 1002, duration=0.1)
            # move to the middle of the screen
            pyautogui.moveTo(800, 400, duration=0.2)

        elif self.action_type == ActionType.PLAY:
            # start hovering all the cards, until wel find the card that we want and then double click it
            x_position = 420
            for x in range(13):
                pyautogui.moveTo(x_position, 1050)
                x_position += 85
                # wait till the hover position is parsed
                time.sleep(1)

                if game.last_hovered_iid == self.card.game_id:
                    # we found the card, click and drag into the field
                    pyautogui.click(x_position, 1000)
                    pyautogui.moveTo(x_position, 600, duration=.4)
                    pyautogui.click()
                    break

        game.last_action_type = self.action_type

    def __str__(self):
        if self.action_type == ActionType.BUTTON:
            return 'pressing {}'.format(self.button)

        elif self.action_type == ActionType.CLICK:
            return 'clicking on location {}'.format(self.position)

        elif self.action_type == ActionType.FORCE_REFRESH:
            return 'just moving around'

        elif self.action_type == ActionType.PLAY:
            return 'playing {}'.format(self.card)

        return 'no known action'
