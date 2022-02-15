#!/usr/bin/env python3

from game.enums.entity_type import EntityType
from game.physical_entity import PhysicalEntity


class Tree(PhysicalEntity):

    def get_type(self) -> EntityType:
        return EntityType.TREE
