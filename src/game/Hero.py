#!/usr/bin/env python3
from src.game.BaseNPC import BaseNPC
from src.game.BaseNPC import Ability


class Hero(BaseNPC):
    def __init__(self, data):
        super().__init__(data)
        self.abilities = {}
        self.__set_abilities()

    def __set_abilities(self):
        self.abilities = {}
        for i, data in self.data["abilities"].items():
            self.abilities[i] = Ability(data)

    def setData(self, data):
        super().setData(data)
        self.__set_abilities()

    def getAbilityPoints(self):
        return self.data["abilityPoints"]

    def getAbilities(self):
        return self.abilities

    def getHasTowerAggro(self):
        return self.data["hasTowerAggro"]

    def getDeaths(self):
        return self.data["deaths"]

    def getDenies(self):
        return self.data["denies"]

    def getGold(self):
        return self.data["gold"]

    def getType(self):
        return self.data["type"]

    def getXp(self):
        return self.data["xp"]
