from enum import Enum, unique

@unique
class DamageType(Enum):
    NONE = 0
    PHYSICAL = 1
    MAGICAL = 2
    PURE = 4
    ALL = 7
    HP_REMOVAL = 8