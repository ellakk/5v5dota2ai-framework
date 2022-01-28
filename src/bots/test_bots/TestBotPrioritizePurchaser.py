from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_bane",
        "npc_dota_hero_batrider",
        "npc_dota_hero_dazzle",
        "npc_dota_hero_wisp",
        "npc_dota_hero_lich",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_brewmaster",
        "npc_dota_hero_doom_bringer",
        "npc_dota_hero_abyssal_underlord",
        "npc_dota_hero_beastmaster",
        "npc_dota_hero_axe",
    ],
}

class TestBotPrioritizePurchaser(BaseBot):
    '''
    Tests:
    - Every hero can buy a stack of tango when in range of shop.
    - Every courier can buy a stack of tango when the courier is in range of shop and its owning hero is not in range.
    - The stacks of tango should become seperate stacks in seperate inventories.
    '''
    
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]

    def __init__(self, world: World) -> None:
        self._world = world
        self._party = party[world.get_team()]

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:

        if self._world.get_game_ticks() == 2:
            hero.buy("item_tango")
        
        if self._world.get_game_ticks() == 3:
            hero.move(0, 0, 0)
        
        if self._world.get_game_ticks() == 20:
            hero.buy("item_tango")