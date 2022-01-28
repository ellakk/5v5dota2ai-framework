from base_bot import BaseBot
from game.world import World
from game.player_hero import PlayerHero

from framework import RADIANT_TEAM, DIRE_TEAM


class Skeleton(BaseBot):
    """A bot inherits from BaseBot"""
    heroes: list[PlayerHero]

    def __init__(self, world: World):
        """The team parameter can be used if the bot has different behaviour depending
        on if it's a Radiant or Dire bot. Possible values are RADIANT_TEAM (2) and DIRE_TEAM (3)."""
        self.party = [
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_pudge",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_lina",
            "npc_dota_hero_chen",
        ]
        self.world = world

    def get_party(self) -> list[str]:
        return self.party

    def initialize(self, heroes: list[PlayerHero]):
        """This method will run once when the game is starting before the actions method
        start getting called. In this method you can setup variables and values
        that will be used later in your code.
        """
        self.heroes = heroes

    def before_actions(self, game_ticks: int) -> None:
        """This method will run before actions run for each hero."""
        pass

    def actions(self, hero: PlayerHero, game_ticks: int):
        """This method will run once for each hero during every gametick. This is the
        starting point for your code commanding the different heroes."""
        if game_ticks == 1:
            hero.move(0, 0, 256)

    def after_actions(self, game_ticks: int) -> None:
        """This method will run after actions has been run for each hero."""
        pass
