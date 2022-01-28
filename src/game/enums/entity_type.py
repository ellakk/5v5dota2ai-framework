from enum import Enum, auto, unique

@unique
class EntityType(Enum):
    ABILITY = auto()
    BUILDING = auto()
    HERO = auto()
    ITEM = auto()
    PHYSICAL_ENTITY = auto()
    PLAYER_HERO = auto()
    TOWER = auto()
    TREE = auto()
    UNIT = auto()
    COURIER = auto()
    RUNE = auto()
