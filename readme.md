#5v5 Dota 2 framework

## About

This is a DotA 2 bot framework intended and needed to be run with the updated [DoTa 2 ADDON dota2ai](https://github.com/ellakk/5v5dota2ai-addon).
It has been developed by Dennis Nilsson and Kalle Lindqvist. It is based on
this [project](https://github.com/lightbringer/dota2ai) by Tobias Mahlmann.

## Requirements

To run this framework you need the following dependencies.

- DotA 2
- DotA 2 5v5 AI addon
- Python 3.7 or above

## Installation

To install this framework all you need to do is clone this repository to your
computer. All requirements and dependencies are in the [requirements file](requirements.txt).

## Running

The framework has to be started before running the DotA 2 addon. You start it by
issuing the following command in the terminal running from src (Rememer to also set src as the root folder in PyCharm):

```console
python framework.py
```

Information about which bot is going to be used for Radiants and Dires, as well as their locations has to be set in the [settings file](setting.json)

## Dota2 - FRAMEWORK V1

## User Manual

### Settings

All of the following settings should be defined in the settings.json file.

| name                                  | default           | type      | description       |
|:--------------------------------------|:------------------|:----------|:------------------|
| base_dir_bots                         | `"bots/"`         | `string`  | Base directory for bot-files. |
| radiant_bot_filename                  | `"BotExample.py"` | `string`  | Python filename for radiant bot including file extension ".py". |
| radiant_bot_class_name                | `"BotExample"`    | `string`  | Radiant bot class name. |
| dire_bot_filename                     | `"BotExample.py"` | `string`  | Python filename for dire bot including file extension ".py". |
| dire_bot_class_name                   | `"BotExample"`    | `string`  | Dire bot class name. |
| native_bots_difficulty                |                   | `string`  | <i>deprecated</i> |
| should_have_pre_game_delay            | `true`            | `boolean` | Whether to keep the pre game state or to skip it. If `true`, the game will keep the default pre game state of 90 seconds. If `false` the game starts immediately. |
| should_dire_be_native_bots            | `false`           | `boolean` | Allows your bot to play as team Radiant against the standard Dota 2 bots. |
| grant_global_vision                   | `false`           | `boolean` | Gives both teams vision of entire map, allowing bots to access information about enemy entities on the map which would otherwise be hidden. |
| spectator_mode                        | `true`            | `boolean` | Allows you to run the game as spectator granting you global vision while the bots have normal vision. |
| number_of_games                       | `1`               | `number`  | Number of times the game will run. While number_of_games is greater than 1 the game will restart when it ends. A game ends when a team wins or the chat command "end" is used. |
| auto_restart_client_on_server_restart | `true`            | `boolean` | If enabled, the Dota addon will run the console command "dota_launch_custom_game Dota2-AI-Framework dota" when it detects the python server has restarted, effectively restarting the addon. |
| max_game_duration                     | `-1`              | `number`  | Sets game time limit. Maximum number of in-game clock minutes per game. If the game has not ended naturally before this target is hit, game end will be simulated. `-1` == no game time limit. |

### Creating bots

A bot is written as a Python class that inherits from BaseBot. BaseBot is an abstract base class, and by inheriting from it, you are forced to implement three methods:

| method | description |
|--------|-----------------------------------------------------------------------------------|
| initialize | Called on the first game tick with a list of the hero entities that belong to this bot. |
| actions    | Called every game tick, once for each hero on the bot's team. In this method, the bot developer decides on what action each hero should take in a particular game tick. |
| get_party  | Should return a list of the heroes that the bot intends to use. |

BaseBot methods with default implementation which can optionally be overridden:

| method | description |
|--------|-----------------------------------------------------------------------------------|
| before_actions | Called every game tick before actions is called for each hero. |
| after_actions | Called every game tick after actions has been called for each hero. |

#### Creating bots: class constructor

The constructor should have a single argument: world. The world parameter is an instance of the world object for the particular team that the bot is on. Radiant and Dire do not share world objects because the teams see different things during the course of the game due to fog of war.

#### Creating bots: game ticks

Game ticks are a fundamental concept in the framework. On each game tick, the game state is updated and each bot controlled hero is allowed to perform a single command. The framework's tick rate is adjustable and ultimately a question of how often the Lua addon sends updates to the Python server. Do not confuse the framework's tick rate with Dota 2's tick rate; they are completely unrelated. The framework's default tick rate is 0.33 seconds which means that a particular hero can never execute more than three commands per second.

#### Creating bots: using the same bot on both teams

It might be the case that you want to use the same bot on both teams and do some things differently depending on what team the bot is on. For example, a bot could define two lists of heroes and return a different one in get_party for each team. To support this use-case the world object has a method, get_team(), that returns the bot's team.

#### Creating bots: using the API

For a hero do something it needs to be issued a command in the actions method. A hero is given a command by calling a method on the hero object. Simple example:

```python
    def actions(self, hero: PlayerHero, game_ticks: int):
        """This method will run once for each hero during every gametick. This is the
        starting point for your code commanding the different heroes."""
        if game_ticks == 1:
            hero.move(0, 0)
```

In the above code, all heroes on this bot's team will move to position (0, 0) on the first game tick and then do nothing else for the rest of the game (assuming that this is the complete actions method). Commands are not "saved" between game ticks, and it's legal to not issue a command in a particular game tick. This means that in this case, the heroes will not have any commands to execute on any game tick above 1. 

However, keep in mind that a single command could have effects in-game beyond the immediate game tick. E.g., a hero will keep moving to its designated position independently of the game ticks until it reaches its position, a different command is issued that stops it from moving to the position in question, or it's killed.

| example methods |
| ---------------|
| attack |                                                                                        |
| move  |
| stop      |         |
| cast |    |
| use_glyph_of_fortification |             |
| use_tp_scroll |                 |
| buy     |                           |
| sell    |                           |

The World object is used to provide game state information that the bot writer might need to make appropriate decisions.

| example methods | description |
|-------------------------------------|-----------------------------------------------------------------------------------------|
| get_team                          | Returns the team that the hero is on (2 for Radiant and 3 for Dire). |
| get_game_time()                   | Returns the current game time in seconds to support taking actions that depend on the game clock. |

For full API documentation see: Documentation/api

### Chat commands

The framework uses in-game chat commands for some functionality. 
To use a chat command, press enter followed by tab. You should now be in the "all" chat channel. In that channel, type your command and press enter. For the commands to work properly, it is recommended that you do not minimize or alt-tab out of the the Dota client immediately after entering a command. Instead, keep the game open until the effect of the command has been seen.


| command | description |
|---------|-------------|
| restart | Restarts the current game. Does not decrease the counter for the number of games in this session which means that you can run this command an unlimited number of times without restarting Dota.
| end     | Ends the current game and decreases the number of remaining games. For example, if number_of_games in settings.json is 2, using the end command once will start a new game and put the number of remaining games to 1. Using end again will end the session.  |
| exit    | Immediately ends the session without taking number_of_games into account.|

### Statistics

The framework collects statistics from the game as it is running. There are three separate collection steps that can be utilized. All three types of statistics are handled by statistics.py and saved to files in the Server/statistics folder, which is created automatically if it doesn't exist. 

The three types of statistics that can be collected are: 
1. Time series data. Some data is suitable for continuous collection to a csv file at predetermined intervals, such as each hero's current kills, deaths and current gold.
2. End screen statistics. When a game of Dota 2 ends, there's an end screen with information about the game and each hero. The framework collects similar data and saves it to a JSON file when the game ends.
3. The state of the game entities at each game tick. This data is already produced during normal operation of the framework and the statistics module is simply saving it to make post-game analysis of the data possible. This data could be used to analyze, for example, the locations of heroes during the game.

Each type of statistics correspond to a single file in the statistics folder. They always have the following names:

| type | identifier | example filename |
|------|----------|---------|
| time series | statistics | 2021_12_20_14_46_4_statistics_0.csv
| end screen  | end_screen | 2021_12_17_16_51_14_end_screen_0.json
| game entities | game_state_dire | 2021_12_20_14_46_4_game_state_dire_0.json
|               | game_state_radiant | 2021_12_20_14_46_4_game_state_radiant_0.json

Timestamps and game numbers are added to each file to create unique file names.

The Dota API allows you to poll the state of the in-game clock. The value of the game clock is always included in the collected data to make it possible to correlate data from different sources. For example, you might find that a particular hero has a lot of gold in the first five minutes of the game by looking at the time series data. You could then look at the game entity data for that same hero during the same time interval. 

Note however that the three types of data collection are performed independently, and the game clock is saved as a float (in seconds). This means that you are unlikely to see the same exact time in any data point. Some kind of processing of the game clock values would therefore be needed to work across files in this manner.

#### CSV Time Series Data: Defining what statistics to collect

To collect statistics that are not currently collected you must do the following:
1. (Re)define the column names for the csv file in Statistics.py.
2. Collect the appropriate statistics and add them to the stats table in the Collect_statistics function in the Lua addon.

```lua
function Statistics:Collect_statistics(radiant_heroes, dire_heroes, game_number)
    local heroes = Utilities:Concat_lists(radiant_heroes, dire_heroes)
    local stats = {}
    local fields = {}
    ...
    return stats
end
```
3. The statistics are sent as a JSON document to the Python server. You must ensure that the to_csv method in Statistics.py correctly translates the statistics that you've gathered into csv that matches the columns that you have defined. 

#### CSV Time Series Data: Defining the collection interval

It's possible to run multiple consecutive games without restarting Dota (defined in settings.json). To account for that possibility, each csv file has a suffix indicating which game it belongs to for that particular instance of Dota.

You can adjust how often statistics are collected by setting the collection_interval variable in the function Python_AI_setup:Set_statistics_collection.

```lua
function Python_AI_setup:Set_statistics_collection(radiant_heroes, dire_heroes)
    --[[
        Creates a timer that runs the 
        Statistics:Collect_and_send_statistics
        function once every @collection_interval seconds.
    ]]
    local collection_interval = 5
end
```

#### CSV Time Series Data: Hero order

Heroes are ordered within a particular game but not between games. 

Example: 
- 'npc_dota_hero_queenofpain' is in position 1 of the hero list in the Dota addon. Statistics related to this hero will be collected first and be placed in the first position for all statistics collected during that particular game.
- In the next game (either through a complete restart of the Dota client or via the restart chat command), 'npc_dota_hero_queenofpain' could be in a different position in the hero list.
- This means that you cannot rely on hero order when analyzing statistics from multiple games.

#### CSV Time Series Data: Restarting the game with the chat command

The framework supports restarting the current game with the "restart" chat command (sent to the "all" chat channel in-game). If this chat command is used, the statistics for the new game will be appended to the same file as the previous game. If this happens, and you still want to save the resulting data, the csv file must be manually processed and split based on the game time timestamps. Moving to the next game with the "end" command will however save the statistics to the next numbered file. 

#### End Screen Statistics: "not implemented"

The data collected to the endscreen JSON file has keys for most things that are found on the real Dota 2 endscreen.
However, due to time constraints, some of them have been given the value "not implemented" to indicate that the actual data is not being gathered from the Dota API. To implement the missing data points, modify this function:

```lua
--[[
    Collects end game statistics for a specific hero.
    These are intended to match what is shown on the actual end-game screen.
]]
---@param hero CDOTA_BaseNPC_Hero
---@return table
function Statistics:Hero_end_game_stats(hero)
    local stats = {}
    stats["id"] = hero:GetPlayerID()
    stats["net_worth"] = "not implemented"
    --[[..]]
    return stats
end
```

#### Game Entity Data: Shape of the JSON document

```json
{
    "123": {
        "game_number": 0,
        "game_time": 0.0,
        "entities": "object with game entities"
    },
    "124": {
        "game_number": 0,
        "game_time": 1.0,
        "entities": "object with game entities"
    },
    "125": {
        "game_number": 0,
        "game_time": 2.0,
        "entities": "object with game entities"
    }
}
```

The string integer key is the game tick where the entities were saved.

#### Game Entity Data: Size

Since the game entities are saved every game tick, the corresponding JSON files can grow quite large. Expect their size to end up being around 100 MB per 10 minutes of game play. Each record is appeneded its JSON file, which should prevent slow down as these files grow large. See the code comments in statistics.py for details on how this is done.

### Generating Documentation

The project uses [pdoc](https://github.com/mitmproxy/pdoc) to generate the API documentation found in the Documentation/api directory. To (re)generate this documentation execute the following command while being located in the Server/src directory:

```
python -m pdoc -o ../../Documentation/api game/player_hero.py game/world.py
```
