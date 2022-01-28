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

class TestBotBuyback(BaseBot):
    '''
    Tests:
    - All radiant heroes move to enemy mid tower.
    - On death they should attempt to use buyback.
    - Buyback should not work when on cooldown.
    - Asserts buyback cooldown time remaining equals 0 when hero is alive.
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
        if self._world.get_team() == RADIANT_TEAM:
            hero.move(500, 500, 0)

            if not hero.is_alive():
                hero.buyback()
            else:
                assert hero.get_buyback_cooldown_time() == 0
