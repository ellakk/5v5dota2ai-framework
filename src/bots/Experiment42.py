# Toggle

import os


class Experiment42:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_medusa",
            "npc_dota_hero_morphling",
            "npc_dota_hero_witch_doctor",
            "npc_dota_hero_pudge",
            "npc_dota_hero_mars"
        ]

        self.hero_toggle_abilities = {
            "npc_dota_hero_medusa": 2,        # Mana shield
            "npc_dota_hero_morphling": 3,     # Shift agility again
            "npc_dota_hero_witch_doctor": 1,  # Voodoo restoration
            "npc_dota_hero_pudge": 1,         # Rot
            "npc_dota_hero_mars": 2           # Bulwark
        }
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 42:")
        self.toggle_assert = True

    def actions(self, hero):
        ability_index = self.hero_toggle_abilities[hero.getName()]

        if hero.getAbilityPoints() > 0:
            hero.level_up(ability_index)
        elif self.world.gameticks == 5 and self.toggle_assert:
            self.toggle_assert = False
            self.assert_toggle_off()
        elif self.world.gameticks == 10:
            hero.cast(ability_index)
        elif self.world.gameticks == 20:
            self.assert_toggle_on()

    def assert_toggle_off(self):
        print("------")
        print("Asserting that toggles are off")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            ability_index = self.hero_toggle_abilities[hero.getName()]
            ability = hero.getAbilities()[str(ability_index)]
            if not ability.getToggleState():
                passed = passed + 1
                print("PASSED: {0} {1} is off".format(
                    hero.getName(), ability.getName()))
            else:
                print("FAILED: {0} {1} is on".format(
                    hero.getName(), ability.getName()))
        print("------")
        if passed == total_tests:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
            raise Exception("FAIL")
        print("{0}/{1} tests passed".format(passed, total_tests))
        print("------")

    def assert_toggle_on(self):
        print("------")
        print("Asserting that toggles are on")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            ability_index = self.hero_toggle_abilities[hero.getName()]
            ability = hero.getAbilities()[str(ability_index)]
            if not ability.getToggleState():
                print("FAILED: {0} {1} is off".format(
                    hero.getName(), ability.getName()))
            else:
                passed = passed + 1
                print("PASS: {0} {1} is on".format(
                    hero.getName(), ability.getName()))
        print("------")
        if passed == total_tests:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(passed, total_tests))
        print("------")
        os._exit(1)
