#!/usr/bin/env python3
from __future__ import annotations
from typing import Union
from base_bot import BaseBot
from game.post_data_interfaces.IRoot import IRoot
from game.world import World
from game.player_hero import CommandProps
from statistics import Statistics


class BotFramework:
    bot_class: type
    world: World
    team: int
    agent: BaseBot
    initialized: bool
    statistics: Statistics

    def __init__(self, bot_class: type, team: int, statistics: Statistics) -> None:
        self.bot_class = bot_class
        self.world = World(team)
        self.team = team
        self.agent = bot_class(self.world)
        self.initialized = False
        self.statistics = statistics

    def get_party(self) -> list[str]:
        if len(self.agent.get_party()) > 5:
            raise Exception("Invalid party: list contains too many hero names.")
        if len(self.agent.get_party()) < 5:
            raise Exception("Invalid party: list contains too few hero names.")
        if len(set(self.agent.get_party())) != 5:
            raise Exception("Invalid party: list contains duplicate hero names.")
        return self.agent.get_party()

    def update_and_receive_commands(self, data: IRoot) -> list[dict[str, CommandProps]]:
        self.update(data)
        self.statistics.save_game_state(data, self.world.get_game_ticks(), self.world.get_team())
        self.generate_bot_commands()
        commands = self.receive_bot_commands()
        return commands

    def update(self, data: IRoot) -> None:
        self.world.update(data["entities"])
        self.world.update_time(data["game_time"])

    def generate_bot_commands(self) -> None:
        if not self.initialized:
            self.agent.initialize(self.world.get_player_heroes())
            self.initialized = True

        game_ticks: int = self.world.get_game_ticks()

        self.agent.before_actions(game_ticks)

        for hero in self.world.get_player_heroes():
            self.agent.actions(hero, game_ticks)

        self.agent.after_actions(game_ticks)

    def receive_bot_commands(self) -> list[dict[str, CommandProps]]:
        commands: list[dict[str, CommandProps]] = []

        for hero in self.world.get_player_heroes():
            command: Union[dict[str, CommandProps], None] = hero.get_command()
            if command:
                commands.append(command)
                hero.clear_and_archive_command()
        return commands

    def create_new_bot_framework(self) -> BotFramework:
        return BotFramework(self.bot_class, self.team)
