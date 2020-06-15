from app.models.action import Action, ActionType


def what_to_do(message) -> [Action]:
    message_type = message["type"]
    print('type: {}'.format(message_type))
    actions = []

    # just press space if we need to do anything
    if message_type == 'GREMessageType_ActionsAvailableReq':
        actions.append(Action())

    # if it is an pay cost action, just auto pay, so just press space
    if message_type == 'GREMessageType_PayCostsReq':
        actions.append(Action())

    # always attack with all, so just press space
    if message_type == "GREMessageType_DeclareAttackersReq":
        actions.append(Action())

    if message_type == "GREMessageType_DeclareBlockersReq":
        actions.append(Action())

    if message_type == 'GREMessageType_PromptReq':
        # just press left of the middle
        actions.append(Action(ActionType.CLICK, position=(2800, 850)))

    # after each action we also wait to wait and move around a bit, this because the logs are refreshed then
    actions.append(Action(ActionType.FORCE_REFRESH))

    return actions
