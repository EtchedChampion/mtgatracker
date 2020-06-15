from app.models.action import Action, ActionType
from app.mtga_app import mtga_watch_app


def what_to_do(message_type, action_type) -> [Action]:
    actions = []

    game = mtga_watch_app.game

    # don't do anything if the game is not started yet, or if it has finished
    if game is None or (game is not None and game.final):
        return actions

    # Do nothing if we are not to make an action
    if game.last_decision_player != game.hero:
        print("opponents turn")
        return actions

    if action_type == "Action":
        if message_type == "GREMessageType_SelectNReq":
            # we need to click one of our cards to discard it
            actions.append(Action(ActionType.CLICK, position=(1009, 1003)))
        elif message_type == "GREMessageType_DeclareBlockersReq":
            actions.append(Action())
        else:
            # check if we have any lands in hand if so play one
            print("game turn number: {}".format(game.turn_number))
            for card in game.hero.hand.cards:
                if game.turn_number not in game.turns_played_land and "Land" in card.card_type:
                    actions.append(Action(ActionType.PLAY, card=card))
                    game.turns_played_land.append(game.turn_number)
                    # we can only play one land so break
                    break

    elif action_type == "Prompt":
        # just press left of the middle
        actions.append(Action(ActionType.CLICK, position=(2800, 850)))

    # elif action_type == "Hover" and game.last_action_type != ActionType.FORCE_REFRESH:
    #     # only doe something if we are not the deciding player and game is not finished
    #     if game is not None and not game.final:
    #         # start from the left in the hand section, and go slowly to the right
    #         actions.append(Action(ActionType.FORCE_REFRESH))

    # if we are not doing anything, press space
    if len(actions) == 0:
        actions.append(Action())

    return actions
