#!/usr/bin/env python3
import os


class Experiment6:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_pudge",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_lina",
            "npc_dota_hero_chen",
        ]
        self.hero_items = {
            "npc_dota_hero_brewmaster": "item_clarity",
            "npc_dota_hero_pudge": "item_dust",
            "npc_dota_hero_abyssal_underlord": "item_smoke_of_deceit",
            "npc_dota_hero_lina": "item_clarity",
            "npc_dota_hero_chen": "item_faerie_fire"
        }
        self.world = world

    def initialize(self, heroes):
        print("Starting Experiment 6:")

    def actions(self, hero):
        if self.world.gameticks == 10:
            self.buy_items(hero)

        if self.world.gameticks == 20:
            self.assert_items_in_inventory(hero)

        if self.world.gameticks == 30:
            self.sell_item(hero)

        if self.world.gameticks == 40:
            self.assert_items_sold()

    def assert_items_sold(self):
        print("------")
        print("Asserting that bought items are no longer in inventory")

        heroes = self.world._get_player_heroes()
        total_tests = 5
        passed = 0
        for hero in heroes:
            items = hero.get_items()
            item = self.hero_items[hero.getName()]
            item_names = [n["name"] for n in items.values() if n]
            if item in item_names:
                print("FAILED: {0} is in {1}'s inventory".format(
                    item, hero.getName()))

            else:
                print("PASSED: {0} is not in {1}'s inventory".format(
                    item, hero.getName()))
                passed = passed + 1

        print("------")
        if passed == total_tests:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(passed, total_tests))
        print("------")
        os._exit(1)

    def sell_item(self, hero):
        slot = None
        item_name = self.hero_items[hero.getName()]
        for item in hero.get_items().values():
            if item and item["name"] == item_name:
                slot = item["slot"]

        hero.sell(slot)

    def buy_items(self, hero):
        item = self.hero_items[hero.getName()]
        hero.buy(item)
        print("Bought item {0} with hero {1}".format(
            item, hero.getName()))

    def assert_items_in_inventory(self, hero):
        items = hero.get_items()
        item = self.hero_items[hero.getName()]
        item_names = [n["name"] for n in items.values() if n]
        if item not in item_names:
            raise Exception("Items missing in inventory, test can't continue")
