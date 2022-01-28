import json

from importlib import import_module
from bot_framework import BotFramework


def test_update_game_state_runtime():
    """Simple test of the game state update function. Test passes if a call to update doesn't casuse a runtime error."""
    with open('tests/game_data.json') as f:
        data = json.loads(f.read())

    module = import_module('bots.BotExample')
    bot_cls = getattr(module, 'BotExample')
    bot_framework = BotFramework(bot_cls)
    bot_framework.update(data)


def test_generate_bot_commands_runtime():
    """Tests if bot commands can be generated without runtime errors."""
    with open('tests/game_data.json') as f:
        data = json.loads(f.read())

    module = import_module('bots.BotExample')
    bot_cls = getattr(module, 'BotExample')
    bot_framework = BotFramework(bot_cls)
    bot_framework.update(data)
    bot_framework.generate_bot_commands()
    bot_framework.generate_bot_commands()
    bot_framework.receive_bot_commands()