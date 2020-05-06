#!/usr/bin/env python3


class BaseEntity:
    def __init__(self, data):
        self.data = data

    def setData(self, data):
        self.data = data

    def getHealth(self):
        return self.data["health"]

    def getMaxHealth(self):
        return self.data["maxHealth"]

    def getName(self):
        return self.data["name"]

    def getOrigin(self):
        return self.data["origin"]

    def getTeam(self):
        return self.data["team"]
