#!/usr/bin/env python3

from src.game.BaseEntity import BaseEntity


class Ability(BaseEntity):
    DAMAGE_TYPE_NONE = 0
    DAMAGE_TYPE_PHYSICAL = 1
    DAMAGE_TYPE_MAGICAL = 2
    DAMAGE_TYPE_PURE = 4
    DAMAGE_TYPE_ALL = 7
    DAMAGE_TYPE_HP_REMOVAL = 8

    DOTA_ABILITY_BEHAVIOR_NONE = 0
    DOTA_ABILITY_BEHAVIOR_HIDDEN = 1
    DOTA_ABILITY_BEHAVIOR_PASSIVE = 2
    DOTA_ABILITY_BEHAVIOR_NO_TARGET = 4
    DOTA_ABILITY_BEHAVIOR_UNIT_TARGET = 8
    DOTA_ABILITY_BEHAVIOR_POINT = 16
    DOTA_ABILITY_BEHAVIOR_AOE = 32
    DOTA_ABILITY_BEHAVIOR_NOT_LEARNABLE = 64
    DOTA_ABILITY_BEHAVIOR_CHANNELLED = 128
    DOTA_ABILITY_BEHAVIOR_ITEM = 256
    DOTA_ABILITY_BEHAVIOR_TOGGLE = 512
    DOTA_ABILITY_BEHAVIOR_DIRECTIONAL = 1024
    DOTA_ABILITY_BEHAVIOR_IMMEDIATE = 2048
    DOTA_ABILITY_BEHAVIOR_AUTOCAST = 4096
    DOTA_ABILITY_BEHAVIOR_OPTIONAL_UNIT_TARGET = 8192
    DOTA_ABILITY_BEHAVIOR_OPTIONAL_POINT = 16384
    DOTA_ABILITY_BEHAVIOR_OPTIONAL_NO_TARGET = 32768
    DOTA_ABILITY_BEHAVIOR_AURA = 65536
    DOTA_ABILITY_BEHAVIOR_ATTACK = 131072
    DOTA_ABILITY_BEHAVIOR_DONT_RESUME_MOVEMENT = 262144
    DOTA_ABILITY_BEHAVIOR_ROOT_DISABLES = 524288
    DOTA_ABILITY_BEHAVIOR_UNRESTRICTED = 1048576
    DOTA_ABILITY_BEHAVIOR_IGNORE_PSEUDO_QUEUE = 2097152
    DOTA_ABILITY_BEHAVIOR_IGNORE_CHANNEL = 4194304
    DOTA_ABILITY_BEHAVIOR_DONT_CANCEL_MOVEMENT = 8388608
    DOTA_ABILITY_BEHAVIOR_DONT_ALERT_TARGET = 16777216
    DOTA_ABILITY_BEHAVIOR_DONT_RESUME_ATTACK = 33554432
    DOTA_ABILITY_BEHAVIOR_NORMAL_WHEN_STOLEN = 67108864
    DOTA_ABILITY_BEHAVIOR_IGNORE_BACKSWING = 134217728
    DOTA_ABILITY_BEHAVIOR_RUNE_TARGET = 268435456
    DOTA_ABILITY_BEHAVIOR_DONT_CANCEL_CHANNEL = 536870912
    DOTA_ABILITY_LAST_BEHAVIOR = 536870912

    DOTA_UNIT_TARGET_TEAM_NONE = 0
    DOTA_UNIT_TARGET_TEAM_FRIENDLY = 1
    DOTA_UNIT_TARGET_TEAM_ENEMY = 2
    DOTA_UNIT_TARGET_TEAM_BOTH = 3
    DOTA_UNIT_TARGET_TEAM_CUSTOM = 4

    DOTA_UNIT_TARGET_NONE = 0
    DOTA_UNIT_TARGET_HERO = 1
    DOTA_UNIT_TARGET_CREEP = 2
    DOTA_UNIT_TARGET_BUILDING = 4
    DOTA_UNIT_TARGET_MECHANICAL = 8
    DOTA_UNIT_TARGET_COURIER = 16
    DOTA_UNIT_TARGET_BASIC = 18
    DOTA_UNIT_TARGET_OTHER = 32
    DOTA_UNIT_TARGET_ALL = 63
    DOTA_UNIT_TARGET_TREE = 64
    DOTA_UNIT_TARGET_CUSTOM = 128

    def __init__(self, data):
        super().__init__(data)

    def getAbilityDamage(self):
        return self.data["abilityDamage"]

    def getAbilityDamageType(self):
        return self.data["abilityDamageType"]

    def getAbilityIndex(self):
        return self.data["abilityIndex"]

    def getAbilityType(self):
        return self.data["abilityType"]

    def getBehavior(self):
        return self.data["behavior"]

    def getCooldownTime(self):
        return self.data["cooldownTime"]

    def getCooldownTimeRemaining(self):
        return self.data["cooldownTimeRemaining"]

    def getLevel(self):
        return self.data["level"]

    def getMaxLevel(self):
        return self.data["maxLevel"]

    def getTargetFlags(self):
        return self.data["targetFlags"]

    def getTargetTeam(self):
        return self.data["targetTeam"]

    def getTargetType(self):
        return self.data["targetType"]

    def getToggleState(self):
        return self.data["toggleState"]
