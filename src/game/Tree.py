#!/usr/bin/env python3

from src.game.BaseEntity import BaseEntity


class Tree(BaseEntity):
    def __init__(self, data):
        data['name'] = 'tree'
        data['team'] = 4
        super().__init__(data)

    def setData(self, data):
        data['name'] = 'tree'
        data['team'] = 4
        super().setData(data)
