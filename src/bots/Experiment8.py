#!/usr/bin/env python3
import os

class Experiment8:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_pudge",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_lina",
            "npc_dota_hero_chen",
        ]
        self.hero_movment_points = {
            "npc_dota_hero_brewmaster": [],
            "npc_dota_hero_pudge": [],
            "npc_dota_hero_abyssal_underlord": [],
            "npc_dota_hero_lina": [],
            "npc_dota_hero_chen": []
        }
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 8:")
        i = 4
        for hero_name in self.party:
            if i > 4:
                i = 0
            for hero in heroes:
                if hero.getName() == self.party[i]:
                    self.hero_movment_points[hero_name] = hero.getOrigin()
            i = i + 1

            
    def actions(self, hero):
        if self.world.gameticks == 5:
            hero.move(*self.hero_movment_points[hero.getName()])

        if self.world.gameticks == 30:
            self.assert_items_used()

    def assert_items_used(self):
        print("------")
        print("")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            if hero.getOrigin() == self.hero_movment_points[hero.getName()]:
                passed = passed + 1
                print("PASSED: {} is in position {}".format(hero.getName(), hero.getOrigin()))
            else:
                print("FAIL: {} is in position {}, not {}".format(hero.getName(), hero.getOrigin(), self.hero_movment_points[hero.getName()]))

        print("------")
        if passed == total_tests:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(passed, total_tests))
        print("------")
        os._exit(1)
