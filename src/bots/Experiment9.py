#!/usr/bin/env python3

import os


class Experiment9:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_mirana", "npc_dota_hero_slardar",
            "npc_dota_hero_clinkz", "npc_dota_hero_brewmaster",
            "npc_dota_hero_alchemist"
        ]
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 9:")

    def actions(self, hero):
        if hero.getAbilityPoints() > 0:
            hero.level_up(0)
        elif self.world.gameticks == 20:
            self.assert_abilities_used()

    def assert_abilities_used(self):
        print("------")
        print("Asserting that abilities has leveled up")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            ability = hero.getAbilities()[str(0)]
            if ability.getLevel() > 0:
                passed = passed + 1
                print("PASSED: {0} has levelled up ability {1}".format(
                    hero.getName(), ability.getName()))
            else:
                print("FAILED: {0} has not levelled up ability {1}".format(
                    hero.getName(), ability.getName()))
        print("------")
        if passed == total_tests:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(passed, total_tests))
        print("------")
        os._exit(1)
