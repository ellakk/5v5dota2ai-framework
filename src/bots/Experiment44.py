# Target Area
# Crystal Maiden's  Crystal Nova
# Alchemist's  Acid Spray
# Enigma Midnight Pulse
# Invoker Sun Strike
# Brewmaster Cinder Brew

import os


class Experiment44:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_crystal_maiden", "npc_dota_hero_alchemist",
            "npc_dota_hero_enigma", "npc_dota_hero_disruptor",
            "npc_dota_hero_brewmaster"
        ]
        self.hero_target_area_abilities = {
            "npc_dota_hero_crystal_maiden": 0,
            "npc_dota_hero_alchemist": 0,
            "npc_dota_hero_enigma": 2,
            "npc_dota_hero_disruptor": 2,
            "npc_dota_hero_brewmaster": 1
        }
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 44:")

    def actions(self, hero):
        ability_index = self.hero_target_area_abilities[hero.getName()]

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks == 15:
            print("Hero {0} casting {1}".format(
                hero.getName(),
                hero.getAbilities()[str(ability_index)].getName()))
            hero.cast_target_area(ability_index, hero.getOrigin())
        elif self.world.gameticks == 20:
            self.assert_abilities_used()

    def assert_abilities_used(self):
        print("------")
        print("Asserting that abilities has been cast")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            ability_index = self.hero_target_area_abilities[hero.getName()]
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
