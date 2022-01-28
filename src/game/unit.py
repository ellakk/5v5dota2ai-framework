#!/usr/bin/env python3
from typing import cast, Union
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IEntity import IEntity
from game.physical_entity import PhysicalEntity
from game.position import Position
from game.post_data_interfaces.IUnit import IUnit

class Unit(PhysicalEntity):

    _attack_range: int
    _attack_damage: int
    _attack_target: Union[str, None]
    _is_attacking: bool
    _level: int
    _mana: int
    _max_mana: int
    _alive: bool
    _blind: bool
    _deniable: bool
    _disarmed: bool
    _dominated: bool
    _rooted: bool
    _name: str
    _health: int
    _max_health: int
    _team: int
    _forward_vector: Position
    _magicimmune: bool

    def update(self, data: IEntity) -> None:
        super().update(data)
        unit_data: IUnit = cast(IUnit, data)
        self._name = unit_data["name"]
        self._attack_range = unit_data["attackRange"]
        self._attack_damage = unit_data["attackDamage"]
        self._attack_target = unit_data["attackTarget"] if "attackTarget" in unit_data else None
        self._is_attacking = unit_data["isAttacking"]
        self._level = unit_data["level"]
        self._mana = unit_data["mana"]
        self._max_mana = unit_data["maxMana"]
        self._alive = unit_data["alive"]
        self._blind = unit_data["blind"]
        self._deniable = unit_data["deniable"]
        self._disarmed = unit_data["disarmed"]
        self._dominated = unit_data["dominated"]
        self._rooted = unit_data["rooted"]
        self._health = unit_data["health"]
        self._max_health = unit_data["maxHealth"]
        self._team = unit_data["team"]
        self._forward_vector = Position(*unit_data["forwardVector"])
        self._magicimmune = unit_data["magicimmune"]

    def get_attack_range(self) -> int:
        return self._attack_range

    def get_attack_damage(self) -> int:
        return self._attack_damage

    def get_attack_target(self) -> Union[str, None]:
        """
        Returns the entity id of the attack target if unit is attacking, `None` otherwise.
        """
        return self._attack_target

    def is_attacking(self) -> bool:
        return self._is_attacking

    def get_level(self) -> int:
        return self._level

    def get_mana(self) -> int:
        """
        Returns current amount of mana.
        """
        return self._mana

    def get_max_mana(self) -> int:
        return self._max_mana

    def is_alive(self) -> bool:
        return self._alive

    def is_blind(self) -> bool:
        return self._blind

    def is_deniable(self) -> bool:
        return self._deniable

    def is_disarmed(self) -> bool:
        return self._disarmed

    def is_dominated(self) -> bool:
        return self._dominated

    def is_rooted(self) -> bool:
        return self._rooted

    def get_health(self) -> int:
        """
        Returns current amount of hp.
        """
        return self._health

    def get_max_health(self) -> int:
        return self._max_health

    def get_name(self) -> str:
        return self._name

    def get_team(self) -> int:
        """
        Returns the team of the unit (2 for Radiant and 3 for Dire).
        """
        return self._team

    def get_forward_vector(self) -> Position:
        return self._forward_vector

    def get_type(self) -> EntityType:
        return EntityType.UNIT

    def set_alive(self, is_alive: bool) -> None:
        self._alive = is_alive

    def is_magic_immune(self) -> bool:
        return self._magicimmune
