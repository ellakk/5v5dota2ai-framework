#!/usr/bin/env python3

from typing import cast
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IAbility import IAbility
from game.post_data_interfaces.IEntity import IEntity
from game.base_entity import BaseEntity


class Ability(BaseEntity):
    _target_flags: int
    _target_team: int
    _ability_damage_type: int
    _toggle_state: bool
    _ability_damage: int
    _behavior: int
    _ability_type: int
    _max_level: int
    _cooldown_time_remaining: float
    _target_type: int
    _ability_index: int
    _type: str
    _name: str
    _level: int
    _mana_cost: int
    _hero_level_required_to_level_up: int

    def update(self, data: IEntity) -> None:
        super().update(data)
        ability_data: IAbility = cast(IAbility, data)
        self._target_flags = ability_data["targetFlags"]
        self._target_team = ability_data["targetTeam"]
        self._ability_damage_type = ability_data["abilityDamageType"]
        self._toggle_state = ability_data["toggleState"]
        self._ability_damage = ability_data["abilityDamage"]
        self._behavior = ability_data["behavior"]
        self._ability_type = ability_data["abilityType"]
        self._max_level = ability_data["maxLevel"]
        self._cooldown_time_remaining = ability_data["cooldownTimeRemaining"]
        self._ability_index = ability_data["abilityIndex"]
        self._type = ability_data["type"]
        self._name = ability_data["name"]
        self._level = ability_data["level"]
        self._mana_cost = ability_data["manaCost"]
        self._hero_level_required_to_level_up = ability_data["heroLevelRequiredToLevelUp"]

    def get_name(self) -> str:
        return self._name

    def get_ability_damage(self) -> int:
        return self._ability_damage

    def get_ability_damage_type(self) -> int:
        return self._ability_damage_type

    def get_ability_index(self) -> int:
        return self._ability_index

    def get_ability_type(self) -> int:
        return self._ability_type

    def get_behavior(self) -> int:
        return self._behavior

    def get_cooldown_time_remaining(self) -> float:
        return self._cooldown_time_remaining

    def get_level(self) -> int:
        return self._level

    def get_max_level(self) -> int:
        return self._max_level

    def get_target_flags(self) -> int:
        return self._target_flags

    def get_target_team(self) -> int:
        return self._target_team

    def get_target_type(self) -> int:
        return self._target_type

    def get_toggle_state(self) -> bool:
        return self._toggle_state

    def get_mana_cost(self) -> int:
        return self._mana_cost

    def get_hero_level_required_to_level_up(self) -> int:
        """
        Returns the hero level required to level up this ability. If the hero's level is less than this value, this ability cannot be leveled up.
        """
        return self._hero_level_required_to_level_up

    def get_type(self) -> EntityType:
        return EntityType.ABILITY
