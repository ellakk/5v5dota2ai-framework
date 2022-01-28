import json

from bot_framework import BotFramework
from framework_util import exit_with_error, load_class, BotClassError
from statistics import Statistics
from webserver import setup_web_server
from pathlib import Path

RADIANT_TEAM = 2
DIRE_TEAM = 3
settings_directory = Path(__file__).parent.parent
settings_filename = settings_directory / 'settings.json'


def load_settings(filename: Path) -> dict:
    try:
        with open(filename) as f:
            settings_data = json.loads(f.read())
        return settings_data
    except FileNotFoundError as fe:
        exit_with_error(f"Couldn't open {settings_filename}.")
    except json.decoder.JSONDecodeError:
        exit_with_error(f"Malformed JSON file: {settings_filename}")


if __name__ == '__main__':
    try:
        settings = load_settings(settings_filename)
        base_dir = settings['base_dir_bots']
        radiant_bot_filename = settings['radiant_bot_filename']
        radiant_bot_class_name = settings['radiant_bot_class_name']
        dire_bot_filename = settings['dire_bot_filename']
        dire_bot_class_name = settings['dire_bot_class_name']
        difficulty = settings['native_bots_difficulty']
        number_of_games = settings['number_of_games']

        radiant_bot = load_class(base_dir, radiant_bot_filename, radiant_bot_class_name)
        dire_bot = load_class(base_dir, dire_bot_filename, dire_bot_class_name)

        statistics = Statistics(number_of_games)

        radiant_bot_framework = BotFramework(radiant_bot, RADIANT_TEAM, statistics)
        dire_bot_framework = BotFramework(dire_bot, DIRE_TEAM, statistics)

        webserver = setup_web_server(settings_filename, radiant_bot_framework, dire_bot_framework,
                                     number_of_games, statistics)
        webserver.run(server='waitress', host="localhost", port=8080, debug=False, quiet=False)
        webserver.close()
    except KeyError as key_error:
        exit_with_error(f"Couldn't open required key from {settings_filename}: {key_error}")
    except BotClassError as bot_error:
        exit_with_error(f"Couldn't import the bot class:\n{bot_error}")
