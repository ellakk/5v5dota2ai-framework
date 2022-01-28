from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IPosition import IPosition

class IPhysicalEntity(IEntity):
    type: str
    origin: IPosition