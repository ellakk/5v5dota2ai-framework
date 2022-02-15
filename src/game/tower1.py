#!/usr/bin/env python3

from game.enums.entity_type import EntityType
from game.building import Building


class Tower(Building):
    
    def get_type(self) -> EntityType:
        return EntityType.TOWER
