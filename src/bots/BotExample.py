#!/usr/bin/env python3

import random
from src.game.Building import Building


class BotExample:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_doom_bringer",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_beastmaster",
            "npc_dota_hero_axe",
        ]
        self.world = world

    def initialize(self, heroes):
        self.top_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_top").getOrigin()
        self.mid_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_mid").getOrigin()
        self.bot_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_bot").getOrigin()

    def actions(self, hero):
        if not hero.isAlive():
            return

        if self.world.gameticks < 5:
            hero.move(-6826, -7261, 256)
            return

        if self.world.gameticks == 5:
            print("Attempting to buy regen")
            self.buy_ring_of_regen(hero)
            return

        if hero.getAbilityPoints() > 0:
            hero.level_up(random.randint(0, 3))
            return

        if hero.getName() == "npc_dota_hero_brewmaster":
            self.actions_brewmaster(hero)

        if hero.getName() == "npc_dota_hero_doom_bringer":
            self.actions_doom(hero)

        if hero.getName() == "npc_dota_hero_abyssal_underlord":
            self.actions_abyssal_underlord(hero)

        if hero.getName() == "npc_dota_hero_beastmaster":
            self.actions_beastmaster(hero)

        if hero.getName() == "npc_dota_hero_axe":
            self.actions_axe(hero)

    def buy_healing_salve(self, hero):
        if hero.getGold() > 110:
            pass

    def buy_ring_of_regen(self, hero):
        hero.buy("item_ring_of_regen")

    def attack_anything_if_in_range(self, hero):
        enemies = self.world.get_enemies_in_attack_range(hero)
        if enemies:
            target = random.choice(enemies)
            hero.attack(self.world.get_id(target))
            return True
        return False

    def attack_building_if_in_range(self, hero):
        if bool(random.getrandbits(1)):
            self.use_ability_on_enemy(hero)
            if hero.command:
                return True
        enemies = self.world.get_enemies_in_range(hero, 700)
        enemies = [e for e in enemies if isinstance(e, Building)]
        if enemies:
            target = enemies[0]
            hero.attack(self.world.get_id(target))
            return True
        return False

    def attack_unit_if_in_range(self, hero):
        if bool(random.getrandbits(1)):
            self.use_ability_on_enemy(hero)
            if hero.command:
                return True

        enemies = self.world.get_enemies_in_range(hero, 500)
        enemies = [e for e in enemies if not isinstance(e, Building)]
        if enemies:
            target = random.choice(enemies)
            hero.attack(self.world.get_id(target))
            return True
        return False

    def use_ability_on_enemy(self, hero):
        abilities = []

        for ability in hero.getAbilities().values():
            if ability.getLevel() < 1:
                continue
            if ability.getAbilityDamageType(
            ) == ability.DOTA_ABILITY_BEHAVIOR_POINT:
                continue
            if ability.getCooldownTimeRemaining() > 0:
                continue
            abilities.append(ability)

        if not abilities:
            print("No abilities for" + hero.getName())
            return

        enemies = self.world.get_enemies_in_range(hero, 500)
        if not enemies:
            return

        ability = random.choice(abilities)
        enemy = random.choice(enemies)

        if (ability.getBehavior()
                & ability.DOTA_ABILITY_BEHAVIOR_UNIT_TARGET) > 0:
            hero.cast(ability.getAbilityIndex(),
                      target=self.world.get_id(enemy))
        else:
            hero.cast(ability.getAbilityIndex(), position=enemy.getOrigin())

    def push_lane(self, hero, fallback_position):
        if not hasattr(hero, "fallback_position"):
            hero.fallback_position = fallback_position

        if not hasattr(hero, "in_lane"):
            hero.in_lane = False

        if not hasattr(hero, "follow_creeps"):
            hero.follow_creeps = []

        if not hasattr(hero, "has_creep_group"):
            hero.has_creep_group = False

        if not hero.in_lane:
            hero.move(*hero.fallback_position)
            if self.world.get_distance_pos(hero.getOrigin(),
                                           hero.fallback_position) < 300:
                hero.in_lane = True
            return

        for creep in hero.follow_creeps:
            if self.world.get_id(creep) and creep.isAlive():
                continue
            hero.follow_creeps.remove(creep)

        if hero.has_creep_group and len(hero.follow_creeps) > 1:
            if self.attack_building_if_in_range(
                    hero) or self.attack_unit_if_in_range(hero):
                return
            self.follow_unit(hero, hero.follow_creeps[0])
        elif hero.has_creep_group and len(hero.follow_creeps) <= 1:
            hero.has_creep_group = False
            hero.follow_creeps = []
        elif not hero.has_creep_group:
            follow_creeps = self.get_closes_creep_group(hero)
            if follow_creeps:
                hero.follow_creeps = follow_creeps
                hero.has_creep_group = True
            else:
                hero.move(*hero.fallback_position)

    def flee_if_tower_aggro(self, hero, safepoint):
        if hero.getHasTowerAggro():
            hero.move(*safepoint)
            return True
        return False

    def close_friendly_creeps(self, hero):
        creeps = self.world.get_friendly_creeps(hero)
        close_creeps = []
        for c in creeps:
            if self.world.get_distance_units(c, hero) < 1000:
                close_creeps.append(c)
        return close_creeps

    # Brew goes mid
    def actions_brewmaster(self, hero):
        if self.flee_if_tower_aggro(hero, self.mid_fallback_point):
            return

        self.push_lane(
            hero,
            self.mid_fallback_point)

    # Doom goes bot
    def actions_doom(self, hero):
        if self.flee_if_tower_aggro(hero, self.bot_fallback_point):
            return
        self.push_lane(
            hero,
            self.bot_fallback_point)

    # Beastmaster goes bot
    def actions_beastmaster(self, hero):
        if self.flee_if_tower_aggro(hero, self.bot_fallback_point):
            return
        self.push_lane(
            hero,
            self.bot_fallback_point)

    # Underlord goes top
    def actions_abyssal_underlord(self, hero):
        if self.flee_if_tower_aggro(hero, self.top_fallback_point):
            return
        self.push_lane(
            hero,
            self.top_fallback_point)

    # Axe goes top
    def actions_axe(self, hero):
        if self.flee_if_tower_aggro(hero, self.top_fallback_point):
            return
        self.push_lane(
            hero,
            self.top_fallback_point)

    def get_closes_creep_group(self, hero):
        creep_group = []
        friendly_creeps = self.world.get_friendly_creeps(hero)
        creeps_by_distance = {}
        for creep in friendly_creeps:
            distance = self.world.get_distance_units(hero, creep)
            creeps_by_distance[distance] = creep

        if not creeps_by_distance:
            return creep_group

        closest_creep_distance = min(creeps_by_distance.keys())
        closest_creep = creeps_by_distance[closest_creep_distance]
        if closest_creep_distance > 700:
            return creep_group

        creeps_by_distance = {}
        for creep in friendly_creeps:
            if creep == closest_creep:
                continue
            distance = self.world.get_distance_units(closest_creep, creep)
            creeps_by_distance[distance] = creep

        creep_group.append(closest_creep)
        for distance in sorted(creeps_by_distance.keys())[:3]:
            creep_group.append(creeps_by_distance[distance])

        return creep_group

    def follow_unit(self, hero, unit):
        hero.move(*unit.getOrigin())
