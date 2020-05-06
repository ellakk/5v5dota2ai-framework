# Target Point

import os


class Experiment43:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_techies",
            "npc_dota_hero_spectre",
            "npc_dota_hero_morphling",
            "npc_dota_hero_lina",
            "npc_dota_hero_mars"
        ]

        self.hero_no_targets_abilities = {
            "npc_dota_hero_techies": 2,    # proximity mines
            "npc_dota_hero_spectre": 0,    # spectral dagger
            "npc_dota_hero_morphling": 0,  # waveform
            "npc_dota_hero_lina": 1,       # light strke array
            "npc_dota_hero_mars": 0,       # Spear of mars
        }
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 43:")

    def actions(self, hero):
        ability_index = self.hero_no_targets_abilities[hero.getName()]

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks == 15:
            hero.cast(ability_index, position=hero.getOrigin())
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
