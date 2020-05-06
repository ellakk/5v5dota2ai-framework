# noTarget
# mirana Starstorm #
# Slardar Slithereen #
# Clinkz Skeleton walk #
# Brewmaster Thunder clap #
# Alchemist  # Unstable concoction
import os


class Experiment41:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_mirana", "npc_dota_hero_slardar",
            "npc_dota_hero_clinkz", "npc_dota_hero_brewmaster",
            "npc_dota_hero_alchemist"
        ]

        self.hero_no_targets_abilities = {
            "npc_dota_hero_mirana": 0,  # Starstorm
            "npc_dota_hero_slardar": 1,  # Slithereen
            "npc_dota_hero_clinkz": 2,  # Skeleton walk
            "npc_dota_hero_brewmaster": 0,  # Thunder clap
            "npc_dota_hero_alchemist": 1  # Unstable concoction
        }
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 41:")

    def actions(self, hero):
        ability_index = self.hero_no_targets_abilities[hero.getName()]

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks > 10 and self.world.gameticks < 20:
            hero.cast(ability_index)
        elif self.world.gameticks == 20:
            self.assert_abilities_used()

    def assert_abilities_used(self):
        print("------")
        print("Asserting that abilities has been cast")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            ability_index = self.hero_no_targets_abilities[hero.getName()]
            ability = hero.getAbilities()[str(ability_index)]
            if ability.getCooldownTimeRemaining() > 0:
                passed = passed + 1
                print("PASSED: {0} has cast ability {1}".format(
                    hero.getName(), ability.getName()))
            else:
                print("FAILED: {0} has not cast ability {1}".format(
                    hero.getName(), ability.getName()))
        print("------")
        if passed == total_tests:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(passed, total_tests))
        print("------")
        os._exit(1)
