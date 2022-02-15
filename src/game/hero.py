#!/usr/bin/env python3
from typing import cast
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IHero import IHero
from game.unit import Unit


class Hero(Unit):

    _has_tower_aggro: bool
    _has_aggro: bool
    _deaths: int

    def update(self, data: IEntity) -> None:
        super().update(data)
        hero_data = cast(IHero, data)

        self._has_tower_aggro = hero_data["hasTowerAggro"]
        self._has_aggro = hero_data["hasAggro"]
        self._deaths = hero_data["deaths"]

    def get_has_tower_aggro(self) -> bool:
        """
        Whether the hero is being attacked by a tower.
        """
        return self._has_tower_aggro

    def get_has_aggro(self) -> bool:
        """
        Whether the hero is being attacked.
        """
        return self._has_aggro

    def get_deaths(self) -> int:
        return self._deaths

    def get_type(self) -> EntityType:
        return EntityType.HERO
