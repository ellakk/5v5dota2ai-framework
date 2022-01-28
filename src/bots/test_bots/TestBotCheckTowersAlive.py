from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from game.tower import Tower
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

class TestBotCheckTowersAlive(BaseBot):
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _dire_towers: list[Tower]
    _radiant_towers: list[Tower]
    _dire_tower1_top: Tower


    def __init__(self, world: World):
        self._world = world
        self._party = party[world.get_team()]

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        # if self._world.get_team() == RADIANT_TEAM:
        #     print(len(self._world.get_allied_towers_of(hero)))

        if self._world.get_game_ticks() >= 50:
            if hero.get_name() == "npc_dota_hero_axe":
                #_radiant_towers = self._world.get_allied_towers_of(hero)
                #_dire_towers = self._world.get_enemy_towers_of(hero)
                #for tower in _radiant_towers:
                    #if tower.get_name() == "dota_goodguys_tower1_top":
                        #print(tower.get_name())
                #for tower in _dire_towers:
                    #print(tower.get_name())
                self._move_axe(hero)


    def _move_axe(self, hero: PlayerHero):
        if not self._axe_already_in_position(hero):
            hero.move(-3000, 5000, 0)

    def _axe_already_in_position(self, hero: PlayerHero) -> bool:
        if hero.get_position().x == -3000:
            if hero.get_position().y == 5000:
                if hero.get_position().z == 0:
                    return True
        return False