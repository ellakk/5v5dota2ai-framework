from enum import Enum, unique

@unique
class UnitTarget(Enum):
    NONE = 0
    HERO = 1
    CREEP = 2
    BUILDING = 4
    MECHANICAL = 8
    COURIER = 16
    BASIC = 18
    OTHER = 32
    ALL = 63
    TREE = 64
    CUSTOM = 128