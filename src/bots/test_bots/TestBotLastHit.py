from typing import Union
from game.unit import Unit
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_puck",
        "npc_dota_hero_pudge",
        "npc_dota_hero_pugna",
        "npc_dota_hero_queenofpain",
        "npc_dota_hero_razor",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_warlock",
        "npc_dota_hero_weaver",
        "npc_dota_hero_windrunner",
        "npc_dota_hero_winter_wyvern",
        "npc_dota_hero_witch_doctor",
    ],
}

class TestBotLastHit(BaseBot):
    '''
    Tests:
    - All heroes should attempt to only get last hits.
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
        self.make_choice(hero)

    def make_choice(self, hero: PlayerHero) -> None:
        if self.hero_name_match_any(hero, ["puck", "pudge"]):
            self.push_lane(hero, "dota_goodguys_tower1_top")
        elif self.hero_name_match_any(hero, ["pugna"]):
            self.push_lane(hero, "dota_goodguys_tower1_mid")
        elif self.hero_name_match_any(hero, ["queenofpain", "razor"]):
            self.push_lane(hero, "dota_goodguys_tower1_bot")
        elif self.hero_name_match_any(hero, ["warlock", "weaver"]):
            self.push_lane(hero, "dota_badguys_tower1_top")
        elif self.hero_name_match_any(hero, ["windrunner"]):
            self.push_lane(hero, "dota_badguys_tower1_mid")
        elif self.hero_name_match_any(hero, ["winter_wyvern", "witch_doctor"]):
            self.push_lane(hero, "dota_badguys_tower1_bot")

    def hero_name_match_any(self, hero: PlayerHero, matches: list[str]) -> bool:
        for match in matches:
            if hero.get_name() == "npc_dota_hero_" + match:
                return True
        return False

    def push_lane(self, hero: PlayerHero, lane_tower_name: str) -> None:
        if self.is_near_allied_creeps(hero):
            creep_to_last_hit: Union[Unit, None] = self.get_creep_to_last_hit(hero)
            if creep_to_last_hit is not None:
                hero.attack(creep_to_last_hit.get_id())
            else:
                hero.move(*self.get_closest_allied_creep(hero).get_position())
        else:
            lane_tower: Union[Unit, None] = self._world.get_unit_by_name(lane_tower_name)
            if lane_tower is not None:
                hero.move(*lane_tower.get_position())

    def get_creep_to_last_hit(self, hero: PlayerHero) -> Union[Unit, None]:
        closest_enemy_creeps = self.get_closest_enemy_creeps(hero)

        for creep in closest_enemy_creeps:
            if creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def is_near_allied_creeps(self, hero: PlayerHero) -> bool:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_allies: list[Unit] = self._world.get_allies_in_range_of(hero, 750)

        for allied in close_allies:
            if allied in creeps:
                return True
        return False

    def get_closest_enemy_creeps(self, hero: PlayerHero) -> list[Unit]:
        creeps: list[Unit] = self._world.get_enemy_creeps_of(hero)
        close_enemy_creeps: list[Unit] = []

        for creep in creeps:
            if self._world.get_distance_between_units(hero, creep) < 500 or self._world.get_distance_between_units(hero, creep) < hero.get_attack_range():
                close_enemy_creeps.append(creep)

        return close_enemy_creeps

    def get_closest_allied_creep(self, hero: PlayerHero) -> Unit:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        creeps_with_distance_to_hero: dict[Unit, float] = {}

        for allied_creep in creeps:
            creeps_with_distance_to_hero[allied_creep] = self._world.get_distance_between_units(hero, allied_creep)

        return min(creeps_with_distance_to_hero.keys(), key=(lambda allied_creep: creeps_with_distance_to_hero[allied_creep]))