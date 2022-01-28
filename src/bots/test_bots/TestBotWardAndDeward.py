from game.position import Position
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM
from game.enums.ward_spots import WardSpotPosition

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

class TestBotWardAndDeward(BaseBot):
    '''
    Tests:
    - Abyssal Underlord should buy one observer ward, move to location and place ward. 
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
                "npc_dota_hero_abyssal_underlord",
            ]):
                hero.buy("item_ward_observer")

        if self._world.get_game_ticks() >= 10:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_abyssal_underlord",
            ]):
               items = hero.get_items()
               chosen_position = Position(2687.12, -3466.10, 0)
               if len(items) and items[0].get_cast_range() >= self._world.get_distance_between_positions(position1 = hero.get_position(), position2 = chosen_position):
                    hero.use_item(0, position = chosen_position)
               else: 
                    hero.move(*chosen_position)
                    if len(items) == 0:
                        hero.move(-4000, -4000, 0)

        if self._world.get_game_ticks() == 5:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_bane",
            ]):
                hero.buy("item_tango")

        if self._world.get_game_ticks() == 6:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_bane",
            ]):
                hero.buy("item_ward_sentry")
            
        if self._world.get_game_ticks() >= 15:
            if self._hero_name_equals_any(hero.get_name(), [
                "npc_dota_hero_bane",
            ]):
                items = hero.get_items()
                chosen_position = Position(2687.12, -3466.10, 0)
                if len(items) == 2 and items[1].get_cast_range() >= self._world.get_distance_between_positions(position1 = hero.get_position(), position2 = chosen_position):
                    hero.use_item(items[1].get_slot(), position = chosen_position)


                else:
                    hero.move(*chosen_position)
                    if len(items) == 1:
                        wards = self._world.get_wards()
                        for ward in wards:
                            if ward.get_team() != hero.get_team():
                                hero.use_item(items[0].get_slot(), ward.get_id())

            return



    def _hero_name_equals_any(self, to_test: str, to_test_against: list[str]) -> bool:
        for value in to_test_against:
            if to_test == value:
                return True
        return False