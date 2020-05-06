#!/usr/bin/env python3

from src.game.BaseNPC import BaseNPC


class Building(BaseNPC):
    def __init__(self, data):
        super().__init__(data)
