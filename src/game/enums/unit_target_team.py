from enum import Enum, unique

@unique
class UnitTargetTeam(Enum):
    NONE = 0
    FRIENDLY = 1
    ENEMY = 2
    BOTH = 3
    CUSTOM = 4