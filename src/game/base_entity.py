#!/usr/bin/env python3


from abc import ABC, abstractmethod

from game.enums.entity_type import EntityType
from game.post_data_interfaces.IEntity import IEntity


class BaseEntity(ABC):
    
    _entity_id: str

    def __init__(self, entity_id: str) -> None:
        self._entity_id = entity_id

    def get_id(self) -> str:
        return self._entity_id

    @abstractmethod
    def get_type(self) -> EntityType:
        pass

    @abstractmethod
    def update(self, data: IEntity):
        pass
