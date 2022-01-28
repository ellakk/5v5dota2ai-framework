import json
from enum import Enum, auto
from bot_framework import BotFramework
from bottle import request, response, Bottle
from pathlib import Path
from statistics import Statistics
from threading import Lock


class ServerState(Enum):
    """
    When a new Dota game starts, settings should be loaded from the /api/settings route before
    game state updates are processed. The server therefore starts in the SETTINGS state
    and only moves to the UPDATE state once the settings have been sent. In the UPDATE state the
    server is allowed to update the game state and run the bot AI.

    HTTP requests from Dota have very long timeouts and are buffered within the game even when this
    server is turned off (the API supposedly supports lowering these timeouts but experimentation
    has shown these to have no effect).

    Restarting the server on the same port and starting a new Dota game can lead to game updates
    from the previous game being received by the server before the settings are requested for the
    new game. By using this state machine, we avoid having to fully restart Dota between matches
    to flush old updates.
    """
    SETTINGS = auto()
    UPDATE = auto()


def setup_web_server(settings_filename: Path, radiant_bot_framework: BotFramework,
                     dire_bot_framework: BotFramework, games_remaining: int,
                     statistics: Statistics) -> Bottle:
    """Defines the web server routes and return the Bottle app instance."""
    app = Bottle()
    state = ServerState.SETTINGS

    # To support ending and restarting games, and to run multiple consecutive games, we need to create
    # new BotFramework objects. A possible issue is that this will be done at the same time as an update
    # is being handled for the current game, possibly corrupting data. To solve this issue two locks
    # are used: radiant_lock and dire_lock. Each lock is acquire when an update is being handled for that
    # team. To create new instances of the framework, both locks must be acquired. The end result should
    # be that any "in flight" updates are always finished before a new game is initiated.
    radiant_lock = Lock()
    dire_lock = Lock()

    @app.get("/api/settings")
    def settings():
        nonlocal state

        if state != ServerState.SETTINGS:
            response.status = 406
            return {'status:': 'error', 'message': 'invalid server state in settings'}

        r_party = radiant_bot_framework.get_party()
        d_party = dire_bot_framework.get_party()
        with open(settings_filename) as f:
            user_settings = json.loads(f.read())

        user_settings['radiant_party_names'] = r_party
        user_settings['dire_party_names'] = d_party
        user_settings['game_number'] = user_settings['number_of_games'] - games_remaining

        state = ServerState.UPDATE
        return json.dumps(user_settings)

    @app.post("/api/game_ended")
    def game_ended():
        nonlocal state, games_remaining, radiant_bot_framework, dire_bot_framework

        if request.content_type != 'application/json':
            response.status = 415
            return {'status': 'error', 'message': 'This API only understands JSON'}

        statistics.end_game_stats(parse_json_in_req(request))

        with radiant_lock, dire_lock:
            state = ServerState.SETTINGS
            games_remaining -= 1

            if games_remaining == 0:
                return {'status': 'done'}
            else:
                radiant_bot_framework = radiant_bot_framework.create_new_bot_framework()
                dire_bot_framework = dire_bot_framework.create_new_bot_framework()
                return {'status': 'restart'}

    @app.post("/api/restart_game")
    def restart_game():
        nonlocal state, radiant_bot_framework, dire_bot_framework

        with radiant_lock, dire_lock:
            state = ServerState.SETTINGS
            radiant_bot_framework = radiant_bot_framework.create_new_bot_framework()
            dire_bot_framework = dire_bot_framework.create_new_bot_framework()
            return {'status': 'restart'}

    @app.post("/api/statistics")
    def collect_statistics():
        if request.content_type != 'application/json':
            response.status = 415
            return {'status': 'error', 'message': 'This API only understands JSON'}

        statistics.save(parse_json_in_req(request))

    @app.post("/api/radiant_update")
    def radiant_update():
        return update_game_state(radiant_bot_framework, state, radiant_lock)

    @app.post("/api/dire_update")
    def dire_update():
        return update_game_state(dire_bot_framework, state, dire_lock)

    return app


def update_game_state(bot_framework, state, bot_framework_lock):
    with bot_framework_lock:
        if state != ServerState.UPDATE:
            response.status = 406
            return {'status:': 'error', 'message': 'invalid server state in update game state'}

        if request.content_type != 'application/json':
            response.status = 415
            return {'status': 'error', 'message': 'This API only understands JSON'}

        parsed_json = parse_json_in_req(request)
        commands = bot_framework.update_and_receive_commands(parsed_json)
        return json.dumps(commands)


def parse_json_in_req(req: request) -> dict:
    """Extracts the JSON content from a Bottle request."""
    # If the JSON document is large (bigger than the Bottle constant MEMFILE_MAX) then
    # requests.json will contain the json as a string, and we need a separate parsing step.
    # Otherwise, request.json will already have parsed the JSON into a dict.
    raw_json = req.json
    parsed_json = json.loads(raw_json) if type(raw_json) == str else raw_json
    return parsed_json
