from typing import cast
from game.base_entity import BaseEntity
from game.position import Position
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class PhysicalEntity(BaseEntity):
    
    _position: Position

    def update(self, data: IEntity) -> None:
        physical_entity_data: IPhysicalEntity = cast(IPhysicalEntity, data)
        self._position = Position(*physical_entity_data["origin"])

    def get_position(self) -> Position:
        return self._position
