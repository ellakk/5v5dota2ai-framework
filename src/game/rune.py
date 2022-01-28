from game.enums.entity_type import EntityType
from game.physical_entity import PhysicalEntity


class Rune(PhysicalEntity):

    def get_type(self) -> EntityType:
        return EntityType.RUNE
