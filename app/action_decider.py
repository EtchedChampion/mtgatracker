from app import mtga_app
from app.models.action import Action, ActionType
from app.mtga_app import mtga_watch_app


def what_to_do(message_type, action_type) -> [Action]:
    print('type: {}'.format(message_type))
    actions = []

    if action_type == "Action":
        if message_type == "GREMessageType_SelectNReq":
            # we need to click one of our cards to discard it
            actions.append(Action(ActionType.CLICK, position=(1009, 1003)))
        else:
            actions.append(Action())

    elif action_type == "Prompt":
        # just press left of the middle
        actions.append(Action(ActionType.CLICK, position=(2800, 850)))

    elif action_type == "Hover":
        # only doe something if we are the deciding player and game is not finished
        if not mtga_watch_app.game.final:
            # start from the left in the hand section, and go slowly to the right
            actions.append(Action(ActionType.FORCE_REFRESH))

    return actions
