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

class TestBotPickUpRune(BaseBot):
    '''
    Tests:
    - Buy bottle, move to bounty rune and pickup bounty rune with bottle.
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

        if self._world.get_game_ticks() == 5:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord"
            ]):
                hero.buy("item_bottle")

        if self._world.get_game_ticks() == 10:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord"
            ]):
                hero.move(-1900, 1400, 0)

        if len(self._world.get_runes()) > 0:
            hero.pick_up_rune(target=self._world.get_runes()[0].get_id())

    def _hero_name_equals_any(self, to_test: str, to_test_against: list[str]) -> bool:
        for value in to_test_against:
            if to_test == value:
                return True
        return False