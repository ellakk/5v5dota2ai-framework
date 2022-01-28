from enum import Enum, unique
from game.position import Position

@unique
class WardSpotPosition(Enum):
    RADIANT_HIGH_GROUND_BOTTOM = Position(-511.625, -3326, 544)
    RADIANT_ABOVE_MID = Position(-2272, -96, 286.2077331543)
    RADIANT_BELOW_MID = Position(2816, -3072, 576)
    RADIANT_JUNGLE_ABOVE_MID = Position(-3456, -1152, 256)
    RADIANT_HIGH_GROUND_MID = Position(-4352, -1024, 544)
    RADIANT_HIGH_GROUND_ROSH = Position(-4096, 1536, 544)
    DIRE_HIGH_GROUND_BOTTOM = Position(4608, 768, 544)
    DIRE_JUNGLE_BELOW_MID = Position(3328, 32, 288)
    DIRE_JUNGLE_ABOVE_MID_1 = Position(-768, 2048, 516.64587402344)
    DIRE_JUNGLE_TOP = Position(-3332, 4368, 263.56723022461)
    DIRE_JUNGLE_ABOVE_MID_2 = Position(-3756, 4256, 328.92147827148)
    DIRE_HIGH_GROUND_TOP = Position(513.619140625, 4102.447265625, 527.99633789063)
    DIRE_SECRET_SHOP = Position(4206.154296875, -1522.5307617188, 144.00366210938)
    DIRE_RUNE_BOTTOM = Position(2048, -776, 527.99731445313)
    DIRE_HIGH_GROUND_ROSH = Position(-2816, 3584, 544)