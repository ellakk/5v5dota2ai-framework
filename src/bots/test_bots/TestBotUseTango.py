from typing import Union
from game.tree import Tree
from game.ability import Ability
from game.hero import Hero
from game.position import Position
from game.unit import Unit
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_pudge",
        "npc_dota_hero_puck",
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

home_position = {
    RADIANT_TEAM: Position(-6826, -7261, 256),
    DIRE_TEAM: Position(6826, 7261, 256),
}

class TestBotUseTango(BaseBot):
    '''
    Tests:
    - All heroes buy tango items at start and use them later when health gets low.
    '''
    
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _should_move_home: dict[str, bool]
    _should_use_tango_countdowns: dict[str, int]
    _noop_countdowns: dict[str, int]
    _home_position: Position

    def __init__(self, world: World) -> None:
        team: int = world.get_team()

        self._world = world
        self._party = party[team]
        self._should_move_home = {}
        self._should_use_tango_countdowns = {}
        self._noop_countdowns = {}
        self._home_position = home_position[team]

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes
        for hero in heroes:
            self._should_move_home[hero.get_name()] = False
            self._should_use_tango_countdowns[hero.get_name()] = 15
            self._noop_countdowns[hero.get_name()] = 0

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        if self._noop_countdowns[hero.get_name()] != 0:
            self._noop_countdowns[hero.get_name()] -= 1
            return

        if self._world.get_game_ticks() < 10 and hero.get_gold() >= 90:
            hero.buy("item_tango")
            return

        self.make_choice(hero)

    def make_choice(self, hero: PlayerHero) -> None:
        
        if hero.get_ability_points() > 0:
            hero.level_up(0)
            return

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
        if hero.get_health() > 0.85 * hero.get_max_health():
            self._should_move_home[hero.get_name()] = False
            self._should_use_tango_countdowns[hero.get_name()] = 15
        elif hero.get_health() < 0.6 * hero.get_max_health():
            self._should_move_home[hero.get_name()] = True

        if self._should_move_home[hero.get_name()]:
            if self._should_use_tango_countdowns[hero.get_name()] == 0:
                if self.use_tango(hero):
                    self._noop_countdowns[hero.get_name()] = 30
                    return
                else:
                    closest_tree: Union[Tree, None] = self.get_closest_tree(hero)
                    if closest_tree is not None:
                        hero.move(*closest_tree.get_position())
                        return
            else:
                self._should_use_tango_countdowns[hero.get_name()] -= 1
            hero.move(*self._home_position)
            return

        lane_tower: Union[Unit, None] = self._world.get_unit_by_name(lane_tower_name)

        if self.is_near_allied_creeps(hero) and not hero.get_has_tower_aggro():
            enemy_hero_to_attack: Union[Hero, None] = self.get_enemy_hero_to_attack(hero)
            creep_to_last_hit: Union[Unit, None] = self.get_creep_to_last_hit(hero)
            creep_to_deny: Union[Unit, None] = self.get_creep_to_deny(hero)
            if enemy_hero_to_attack is not None\
            and enemy_hero_to_attack.get_health() < 0.5 * enemy_hero_to_attack.get_max_health():
                ability: Ability = hero.get_abilities()[0]
                if ability.get_cooldown_time_remaining() == 0:
                    hero.cast_target_unit(ability.get_ability_index(), enemy_hero_to_attack.get_id())
                else:
                    hero.attack(enemy_hero_to_attack.get_id())

            elif creep_to_last_hit is not None:
                hero.attack(creep_to_last_hit.get_id())
            elif creep_to_deny is not None:
                hero.attack(creep_to_deny.get_id())
            elif hero.get_has_aggro():
                if lane_tower is not None:
                    hero.move(*lane_tower.get_position())
            elif enemy_hero_to_attack is not None:
                hero.attack(enemy_hero_to_attack.get_id())
            elif self.should_move_closer_to_allied_creeps(hero):
                self.follow(hero, self.get_closest_allied_creep(hero))
            else:
                self.stop(hero)
        else:
            if lane_tower is not None:
                hero.move(*lane_tower.get_position())

    def use_tango(self, hero: PlayerHero) -> bool:
        tango_slot: int = self.get_tango_slot(hero)
        if tango_slot >= 0:
            tree: Union[Tree, None] = self.get_closest_tree(hero)
            if tree:
                hero.use_item(tango_slot, target = tree.get_id())
                return True
        
        return False


    def get_tango_slot(self, hero: PlayerHero) -> int:
        for item in hero.get_items():
            if item.get_name() == "item_tango":
                return item.get_slot()
        
        return -1

    def get_closest_tree(self, hero: PlayerHero) -> Union[Tree, None]:
        closest_trees: list[Tree] = self._world.get_trees_in_range_of(hero, 900)

        closest_trees.sort(key=lambda tree: self._world.get_distance_between_entities(hero, tree))

        if closest_trees:
            return closest_trees[0]

    def stop(self, hero: PlayerHero) -> None:
        hero.move(*hero.get_position())

    def follow(self, hero: PlayerHero, to_follow: Unit) -> None:
        hero.move(*to_follow.get_position())

    def should_move_closer_to_allied_creeps(self, hero: PlayerHero) -> bool:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_enemies: list[Unit] = self._world.get_enemies_in_range_of(hero, 500)

        for enemy in close_enemies:
            if enemy in creeps:
                return False
        return True

    def get_creep_to_deny(self, hero: PlayerHero) -> Union[Unit, None]:
        closest_allied_creeps = self.get_closest_allied_creeps(hero)

        closest_allied_creeps.sort(key=lambda creep: self._world.get_distance_between_units(hero, creep))

        for creep in closest_allied_creeps:
            if creep.is_deniable() and creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def get_closest_allied_creeps(self, hero: PlayerHero) -> list[Unit]:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_allied_creeps: list[Unit] = []

        for creep in creeps:
            if self._world.get_distance_between_units(hero, creep) < 600:
                close_allied_creeps.append(creep)

        return close_allied_creeps

    def get_enemy_hero_to_attack(self, hero: PlayerHero) -> Union[Hero, None]:
        enemy_heroes: list[Hero] = self.get_closest_enemy_heroes(hero)
        heroes_with_hp: dict[Hero, int] = {}

        for enemy_hero in enemy_heroes:
            heroes_with_hp[enemy_hero] = enemy_hero.get_health()

        if len(heroes_with_hp) == 0:
            return

        return min(heroes_with_hp.keys(), key=(lambda enemy_hero: heroes_with_hp[enemy_hero]))
        
    def get_closest_enemy_heroes(self, hero: PlayerHero) -> list[Hero]:
        enemy_heroes: list[Hero] = self._world.get_enemy_heroes_of(hero)
        close_enemy_heroes: list[Hero] = []

        for enemy_hero in enemy_heroes:
            if self._world.get_distance_between_units(hero, enemy_hero) < 1250:
                close_enemy_heroes.append(enemy_hero)

        return close_enemy_heroes

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