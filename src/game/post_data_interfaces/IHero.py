from game.post_data_interfaces.IUnit import IUnit

class IHero(IUnit):
    hasTowerAggro: bool
    hasAggro: bool
    deaths: int
