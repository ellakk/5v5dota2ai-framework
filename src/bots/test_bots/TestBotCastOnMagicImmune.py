from typing import Union
from game.physical_entity import PhysicalEntity
from game.rune import Rune
from game.enums.ability_behavior import AbilityBehavior
from game.courier import Courier
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

class TestBotCastOnMagicImmune(BaseBot):
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

    def get_closest_enemy_heroes(self, hero: PlayerHero) -> list[Hero]:
        enemy_heroes: list[Hero] = self._world.get_enemy_heroes_of(hero)
        close_enemy_heroes: list[Hero] = []

        for enemy_hero in enemy_heroes:
            if self._world.get_distance_between_units(hero, enemy_hero) < 1250:
                close_enemy_heroes.append(enemy_hero)

        return close_enemy_heroes

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        hero_to_attack = self._world.get_unit_by_name("npc_dota_hero_abyssal_underlord")
        
        if self._world.get_game_ticks() == 4:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_bane"
            ]):
                hero.level_up(2)

        if self._world.get_game_ticks() == 5:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord"
            ]):
                hero.buy("item_ogre_axe")

        if self._world.get_game_ticks() == 6:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord"
            ]):
                hero.buy("item_mithril_hammer")

        if self._world.get_game_ticks() == 7:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord"
            ]):
                hero.buy("item_recipe_black_king_bar")

        if self._world.get_game_ticks() == 10:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord", 
                "npc_dota_hero_bane",
            ]):
                hero.move(-1900, 1400, 0)

        if self._world.get_game_ticks() >= 30:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_bane"
            ]) :
                if hero_to_attack is None:
                    hero.move(-1900, 1400, 0)

                else: 
                    hero.attack(hero_to_attack.get_id())

            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord"
            ]):

                if hero.get_has_aggro():
                    hero.use_item(0)

                else:
                    hero.move(-1900, 1400, 0)
        
        if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_bane"
            ]) :
            
            if hero.is_attacking() and hero_to_attack.is_magic_immune():
                hero.cast_target_unit(2, hero_to_attack.get_id())
                print("Bane tried to cast spell on target but was magic immune")


        

    def _hero_name_equals_any(self, to_test: str, to_test_against: list[str]) -> bool:
        for value in to_test_against:
            if to_test == value:
                return True
        return False