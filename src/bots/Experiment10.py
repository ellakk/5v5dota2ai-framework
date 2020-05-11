#!/usr/bin/env python3

import os
from src.game.Building import Building
from src.game.Tree import Tree


class Experiment10:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_lina", "npc_dota_hero_vengefulspirit",
            "npc_dota_hero_omniknight", "npc_dota_hero_chen",
            "npc_dota_hero_clinkz"
        ]
        self.world = world
        self.passed_heroes = []

    def initialize(self, wheroes):
        print("Starting Experiment 10:")

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
        if len(self.passed_heroes) == 5 or self.world.gameticks > 500:
            self.print_end()

        if hero.getName() in self.passed_heroes:
            return

        if hero.isAttacking():
            self.passed_heroes.append(hero.getName())

        eid = self.get_closest_enemy(hero)
        if eid:
            hero.attack(eid)

    def print_end(self):
        print("------")
        for hero in self.passed_heroes:
            print("PASSED: {0} has auto-attacked".format(hero))
        if len(self.passed_heroes) == 5:
            print("TEST PASSED:")
        else:
            print("TEST FAILED:")
        print("{0}/{1} tests passed".format(len(self.passed_heroes), 5))
        os._exit(1)
