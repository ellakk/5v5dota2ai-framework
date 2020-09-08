#!/usr/bin/env python3

class Skeleton:
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_pudge",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_lina",
            "npc_dota_hero_chen",
        ]
        self.world = world


    def initialize(self, heroes):
        '''This method will run once when the game is starting before the actions method
        start getting called. In this method you can setup variables and values
        that will be used later in your code.
        '''
        print("Initializing Skeleton bot with the following heroes:")
        for hero in heroes:
            hero.getName()

    def actions(self, hero):
        '''This method will run once for each hero during every gametick. This is the
        starting point for your code commanding the different heroes.
        '''
        # I'ts good to wait a few gameticks until we issue the first command
        if self.world.gameticks == 5:
            hero.move(0, 0, 256)
