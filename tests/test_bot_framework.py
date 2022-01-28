import json

from importlib import import_module
from src.bot_framework import BotFramework


def test_update_game_state_runtime():
    """Simple test of the game state update function. Only makes sure that it doesn't cause a runtime error.
    Note: does not in any way verify that update does what it's supposed to do."""
    with open('game_data.json') as f:
        data = json.loads(f.read())

    module = import_module('src.bots.BotExample')
    bot_cls = getattr(module, 'BotExample')
    bot_framework = BotFramework(bot_cls)
    bot_framework.update(data)

