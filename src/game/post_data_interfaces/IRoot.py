from typing import TypedDict
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class IRoot(TypedDict):
    entities: dict[str, IPhysicalEntity]
    game_time: float
