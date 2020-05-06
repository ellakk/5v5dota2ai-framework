import json
import sys
from library.bottle.bottle import run, post, get, request

from src.BotFramework import BotFramework

BOTNAME = "BotExample"
if len(sys.argv) > 2 and sys.argv[1] == "--bot":
    BOTNAME = sys.argv[2]
exec("from src.bots.{0} import {0}".format(BOTNAME))
exec("FRAMEWORK = BotFramework({0})".format(BOTNAME))


@get("/api/party")
def party():
    global FRAMEWORK
    return json.dumps(FRAMEWORK.get_party())


@post("/api/chat")
def chat():
    postdata = request.body.read()

    # print(postdata)
    return json.dumps("ok")


@post("/api/update")
def update():
    post_data = request.body.read()
    # Dump data to file
    f = open("gamedata.txt", "w+")
    f.write(post_data.decode("utf-8"))
    f.close()

    world = json.loads(post_data)

    FRAMEWORK.update(world)
    FRAMEWORK.generate_bot_commands()
    commands = FRAMEWORK.receive_bot_commands()

    return json.dumps(commands)


run(host="localhost", port=8080, debug=False, quiet=True)
