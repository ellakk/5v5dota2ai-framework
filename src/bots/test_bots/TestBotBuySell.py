from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_brewmaster",
        "npc_dota_hero_doom_bringer",
        "npc_dota_hero_abyssal_underlord",
        "npc_dota_hero_beastmaster",
        "npc_dota_hero_axe",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_bane",
        "npc_dota_hero_batrider",
        "npc_dota_hero_dazzle",
        "npc_dota_hero_wisp",
        "npc_dota_hero_lich",
    ],
}

class TestBotBuySell(BaseBot):
    '''
    Tests:
    - brewmaster, doom_bringer, axe, bane and batrider should buy 5 tango stacks.
    - abyssal_underlord, beastmaster, dazzle, wisp and lich should buy 5 branches.
    - brewmaster, doom_bringer, axe, bane and batrider should sell tango stack.
    - abyssal_underlord, beastmaster, dazzle, wisp and lich should sell all branches.
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
        if game_ticks >= 1 and game_ticks <= 5:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_brewmaster",
                "npc_dota_hero_doom_bringer",
                "npc_dota_hero_axe",
                "npc_dota_hero_bane",
                "npc_dota_hero_batrider",
            ]):
                hero.buy("item_tango")
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord",
                "npc_dota_hero_beastmaster",
                "npc_dota_hero_dazzle",
                "npc_dota_hero_wisp",
                "npc_dota_hero_lich"
            ]):
                hero.buy("item_branches")
        
        if self._world.get_game_ticks() >= 15:
            items = hero.get_items()
            if len(items):
                hero.sell(items[0].get_slot())

    def _hero_name_equals_any(self, to_test: str, to_test_against: list[str]) -> bool:
        for value in to_test_against:
            if to_test == value:
                return True
        return False