from typing import Any, Union

from game.post_data_interfaces.IItem import IItem
from game.post_data_interfaces.IUnit import IUnit


class ICourier(IUnit):
    items: dict[str, Union[IItem, list[Any]]]
    inRangeOfHomeShop: bool
    inRangeOfSecretShop: bool
