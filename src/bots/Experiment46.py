# Vector Targeting

# Grimstroke (hero) - Stroke of faith
# Pangolier (hero) - Swashbuckle
# Dark See (hero) - Wall of replica
# Void Spirit (hero) - Aether remnant
# Mars - Gods reburke
import os


class Experiment46:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_grimstroke",
            "npc_dota_hero_pangolier",
            "npc_dota_hero_dark_seer",
            "npc_dota_hero_void_spirit",
            "npc_dota_hero_mars",
        ]
        self.world = world

        self.hero_target_abilities = {
            "npc_dota_hero_grimstroke": 0,  # Stroke of faith
            "npc_dota_hero_pangolier": 0,  # Swashbuckle
            "npc_dota_hero_dark_seer": 0,  # Vacuum
            "npc_dota_hero_void_spirit": 0,  # Aether remnant
            "npc_dota_hero_mars": 1  # Gods rebuke
        }

    def initialize(self, heroes):
        print("Starting Experiment 46:")

    def actions(self, hero):
        ability_index = self.hero_target_abilities[hero.getName()]

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks == 15:
            print("Hero {0} casting {1}".format(
                hero.getName(),
                hero.getAbilities()[str(ability_index)].getName()))
            hero.cast_target_point(ability_index, hero.getOrigin())
        elif self.world.gameticks == 20:
            self.assert_abilities_used()

    def assert_abilities_used(self):
        print("------")
        print("Asserting that vector-abilities has been cast")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            ability_index = self.hero_target_abilities[hero.getName()]
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
