from random import choice
from game.hero import Hero
from game.position import Position
from game.unit import Unit
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_visage",
        "npc_dota_hero_void_spirit",
        "npc_dota_hero_warlock",
        "npc_dota_hero_weaver",
        "npc_dota_hero_windrunner",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_winter_wyvern",
        "npc_dota_hero_witch_doctor",
        "npc_dota_hero_skeleton_king",
        "npc_dota_hero_grimstroke",
        "npc_dota_hero_zuus",
    ],
}

meetPosition: Position = Position(1257, -1274, 0)

class TestBotItemTargetRestricted(BaseBot):
    '''
    Heroes should be able to cast "item_cyclone" on self and on enemies, but not on allies.

    Requirements:
    - Each radiant hero needs to be given an "item_cyclone".

    Tests:
    - All radiant heroes should attempt to cast cyclone on random allied hero and fail.
    - All radiant heroes should successfully cast cyclone on themself.
    - Radiant and dire heroes should move to the center of the map and all radiant heroes should successfully cast cyclone on random enemy hero.
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
            close_enemies: list[Unit] = self._world.get_enemies_in_attack_range_of(hero)
            enemy_heroes: list[Hero] = self._world.get_enemy_heroes_of(hero)
            close_enemy_heroes: list[Hero] = []
            for close_enemy in close_enemies:
                if close_enemy in enemy_heroes:
                    close_enemy_heroes.append(close_enemy)

            if game_ticks == 5:
                allies: list[Unit] = self._world.get_allies_in_range_of(hero, 1200)
                for ally in allies:
                    if isinstance(ally, PlayerHero):
                        hero.use_item(0, ally.get_id())
            elif game_ticks == 8:
                hero.use_item(0, hero.get_id())
            elif game_ticks == 12:
                hero.move(*meetPosition)
            elif close_enemy_heroes:
                hero.use_item(0, choice(close_enemies).get_id())

        else:
            hero.move(*meetPosition)
