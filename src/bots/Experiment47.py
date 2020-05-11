# Target Point or Unit (combination)
# Sand King's  Burrowstrike
# Nature's Prophet's  Sprout (hero furion)
# Lina's  Dragon Slave.
# Lion Earth Spike
# Meepo Poof
import os
from src.game.Building import Building
from src.game.Tree import Tree


class Experiment47:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_sand_king",
            "npc_dota_hero_furion",
            "npc_dota_hero_lina",
            "npc_dota_hero_lion",
            "npc_dota_hero_zuus",
        ]
        self.world = world
        self.hero_target_abilities = {
            "npc_dota_hero_sand_king": 0,  # Dragon slave enemy
            "npc_dota_hero_furion": 0,  # Magic missle enemy
            "npc_dota_hero_lina": 0,  # Heavenly grace friendly
            "npc_dota_hero_lion": 0,  # Penitence enemy
            "npc_dota_hero_zuus": 1  # Death pact enemy
        }
        self.passed_heroes = []
        self.passed_heroes1 = []

    def initialize(self, wheroes):
        print("Starting Experiment 47:")

    def validate_ability_used(self, hero, index):
        if hero.getAbilities()[str(index)].getCooldownTimeRemaining() > 0:
            self.passed_heroes.append(hero.getName())

    def validate_ability_used1(self, hero, index):
        if hero.getAbilities()[str(index)].getCooldownTimeRemaining() > 0:
            self.passed_heroes1.append(hero.getName())

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
        if (len(self.passed_heroes) == 5 and len(self.passed_heroes1) == 5) or self.world.gameticks > 1000:
            self.print_end()

        ability_index = self.hero_target_abilities[hero.getName()]

        if not hero.getName() in self.passed_heroes:
            self.validate_ability_used(hero, ability_index)

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks == 10:
            hero.cast_target_point(ability_index, hero.getOrigin())
        elif self.world.gameticks > 20:
            eid = self.get_closest_enemy(hero)
            if eid:
                if not hero.getName() in self.passed_heroes1:
                    self.validate_ability_used1(hero, ability_index)
                hero.cast_target_unit(ability_index, eid)

    def print_end(self):
        print("------")
        for hero in self.passed_heroes:
            print("PASSED: {0} cast ability point target in slot {1}".format(
                hero, self.hero_target_abilities[hero]))
        if len(self.passed_heroes) == 5:
            print("TEST PASSED ABILITY POINT TARGET:")
        else:
            print("TEST FAILED ABILITY POINT TARGET:")
        print("{0}/{1} tests passed".format(len(self.passed_heroes), 5))

        print("------")
        for hero in self.passed_heroes1:
            print("PASSED: {0} cast ability unit target in slot {1}".format(
                hero, self.hero_target_abilities[hero]))
        if len(self.passed_heroes1) == 5:
            print("TEST PASSED ABILITY UNIT TARGET:")
        else:
            print("TEST FAILED ABILITY UNIT TARGET::")
        print("{0}/{1} tests passed".format(len(self.passed_heroes1), 5))
        os._exit(1)
