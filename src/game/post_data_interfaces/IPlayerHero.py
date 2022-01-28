from typing import Any, Union
from game.post_data_interfaces.IAbility import IAbility
from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IItem import IItem

class IPlayerHero(IHero):
    denies: int
    abilityPoints: int
    abilities: dict[str, IAbility]
    xp: int
    gold: int
    courier_id: str
    buybackCost: int
    buybackCooldownTime: float
    tpScrollAvailable: bool
    tpScrollCooldownTime: float
    tpScrollCharges: int
    items: dict[str, Union[IItem, list[Any]]]
    stashItems: dict[str, Union[IItem, list[Any]]]
    inRangeOfHomeShop: bool
    inRangeOfSecretShop: bool
