#!/usr/bin/env python3

from game.enums.entity_type import EntityType
from game.unit import Unit


class Building(Unit):

    def get_type(self) -> EntityType:
        return EntityType.BUILDING
