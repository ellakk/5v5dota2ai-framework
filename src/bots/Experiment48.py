# Combination of Target Unit and Target Area
# Sven's  Storm Hammer
# Oracle's  Fortune's End
# Winter Wyvern's  Winter's Curse.
import os
from src.game.Building import Building
from src.game.Tree import Tree


class Experiment48:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_sven",
            "npc_dota_hero_oracle",
            "npc_dota_hero_lina",
            "npc_dota_hero_chen",
            "npc_dota_hero_clinkz",
        ]
        self.world = world
        self.hero_target_abilities = {
            "npc_dota_hero_sven": 0,  # Storm hammer
            "npc_dota_hero_oracle": 0,  # Fortune end
            "npc_dota_hero_lina": 0,
            "npc_dota_hero_chen": 0,
            "npc_dota_hero_clinkz": 0
        }
        self.passed_heroes = []

    def initialize(self, wheroes):
        print("Starting Experiment 48:")

    def validate_ability_used(self, hero, index):
        if hero.getAbilities()[str(index)].getCooldownTimeRemaining() > 0:
            self.passed_heroes.append(hero.getName())

    def get_closest_enemy(self, hero):
        enemy_id = None
        enemy_distance = 10000000000000

        for entid, ent in self.world.entities.items():
            if ent.getTeam() == hero.getTeam():
                continue
            if isinstance(ent, Building):
                continue
            if isinstance(ent, Tree):
                continue
            if self.world.get_distance_units(hero, ent) < enemy_distance:
                enemy_id = entid
                enemy_distance = self.world.get_distance_units(hero, ent)

        if enemy_id:
            return int(enemy_id)

    def actions(self, hero):
        if len(self.passed_heroes) == 5 or self.world.gameticks > 1000:
            self.print_end()

        if hero.getName() in self.passed_heroes:
            return

        ability_index = self.hero_target_abilities[hero.getName()]
        self.validate_ability_used(hero, ability_index)

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks > 5:
            eid = self.get_closest_enemy(hero)
            if eid:
                hero.cast_target_unit(ability_index, eid)

    def print_end(self):
        print("------")
        for hero in self.passed_heroes:
            print("PASSED: {0} cast ability in slot {1}".format(
                hero, self.hero_target_abilities[hero]))
        if len(self.passed_heroes) == 5:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(len(self.passed_heroes), 5))
        os._exit(1)
