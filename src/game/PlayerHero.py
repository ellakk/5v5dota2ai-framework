#!/usr/bin/env python3

from src.game.Hero import Hero


class PlayerHero(Hero):
    def __init__(self, data):
        super().__init__(data)
        self.commands = [
            "ATTACK",
            "MOVE",
            "CAST",
            "BUY",
            "SELL",
            "USE_ITEM",
            "LEVELUP",
            "NOOP",
        ]
        self.command = None
        self.commands = []

    def get_command(self):
        return self.command

    def get_items(self):
        return self.data['items']

    def clear_and_archive_command(self):
        if self.command:
            self.commands.append(self.command)
            self.command = None

    def attack(self, target):
        self.command = {
            self.getName(): {
                "command": "ATTACK",
                "target": target
            }
        }

    def move(self, x, y, z):
        self.command = {
            self.getName(): {
                "command": "MOVE",
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast(self, ability, target=-1, position=[-1, -1, -1]):
        x, y, z = position
        self.command = {
            self.getName(): {
                "command": "CAST",
                "ability": ability,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def buy(self, item):
        self.command = {self.getName(): {"command": "BUY", "item": item}}

    def sell(self, slot):
        self.command = {self.getName(): {"command": "SELL", "slot": slot}}

    def use_item(self, slot, target=-1, position=[-1, -1, -1]):
        x, y, z = position
        self.command = {
            self.getName(): {
                "command": "USE_ITEM",
                "slot": slot,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def level_up(self, abilityIndex):
        self.command = {
            self.getName(): {
                "command": "LEVELUP",
                "abilityIndex": abilityIndex
            }
        }

    def noop(self):
        self.command = {self.getName(): {"command": "NOOP"}}

    def cast_toggle(self, abilityIndex):
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_TOGGLE",
                "ability": abilityIndex,
            }
        }

    def cast_no_target(self, abilityIndex):
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_NO_TARGET",
                "ability": abilityIndex,
            }
        }

    def cast_target_point(self, abilityIndex, position):
        x, y, z = position
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_NO_TARGET",
                "ability": abilityIndex,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_area(self, abilityIndex, position):
        x, y, z = position
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_TARGET_AREA",
                "ability": abilityIndex,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_unit(self, abilityIndex, target):
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_TARGET_UNIT",
                "ability": abilityIndex,
                "target": target
            }
        }

    def cast_vector_targeting(self, abilityIndex, position):
        x, y, z = position
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_VECTOR_TARGETING",
                "ability": abilityIndex,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_unit_aoe(self, abilityIndex, target):
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_TARGET_UNIT_AOE",
                "ability": abilityIndex,
                "target": target
            }
        }

    def cast_combo_target_point_unit(self,
                                     abilityIndex,
                                     target=-1,
                                     position=[-1, -1, -1]):
        x, y, z = position
        self.command = {
            self.getName(): {
                "command": "CAST_ABILITY_TARGET_COMBO_TARGET_POINT_UNIT",
                "ability": abilityIndex,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }
