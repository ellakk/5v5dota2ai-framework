from abc import ABC, abstractmethod
from game.player_hero import PlayerHero


class BaseBot(ABC):

    @abstractmethod
    def get_party(self) -> list[str]:
        pass

    @abstractmethod
    def initialize(self, heroes: list[PlayerHero]) -> None:
        pass

    def before_actions(self, game_ticks: int) -> None:
        pass

    @abstractmethod
    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        pass

    def after_actions(self, game_ticks: int) -> None:
        pass
