from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_brewmaster",
        "npc_dota_hero_doom_bringer",
        "npc_dota_hero_abyssal_underlord",
        "npc_dota_hero_beastmaster",
        "npc_dota_hero_axe",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_bane",
        "npc_dota_hero_batrider",
        "npc_dota_hero_dazzle",
        "npc_dota_hero_wisp",
        "npc_dota_hero_lich",
    ],
}


class TestBotBuySpecialItem(BaseBot):

    '''
    Tests:
    - Move Axe to secret shop and buy components to finish shivas guard.
    - Move Axe and Bane to river and let Bane attack Axe.
    - Let Axe use Shivas Guard to check if the item work properly with its active spell and passive bonus.
    '''
    
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _boughtShivas: bool
    _axeIsClose: bool
    _visitedSecretShop: bool

    def __init__(self, world: World) -> None:
        self._world = world
        self._party = party[world.get_team()]
        self._boughtShivas = False
        self._axeIsClose = False
        self._visitedSecretShop = False
        self._boughtShoes = False
        self._usedShivasGuard = False

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        if hero.get_name() == "npc_dota_hero_axe":
            if self._boughtShivas is False:
                hero.buy("item_recipe_shivas_guard")
                self._boughtShivas = True
            elif self._boughtShoes is False:
                hero.buy("item_boots")
                self._boughtShoes = True

        if game_ticks >= 15: 
            if hero.get_name() == "npc_dota_hero_axe":
                if self._visitedSecretShop is False:
                    self._move_to_secret_shop(hero)
                else:
                    if len(hero.get_items()) == 3:
                        print(len(hero.get_items()))
                        hero.buy("item_mystic_staff")
                    elif hero.get_has_aggro():
                        if self._usedShivasGuard is False:
                            hero.use_item(1)
                            self._usedShivasGuard = True
                        else:
                            hero.move(400, 400, 0)
                    else:
                        self._move_axe(hero)


            if hero.get_name() == "npc_dota_hero_bane":
                if self._world.get_enemies_in_attack_range_of(hero):
                    self._axeIsClose = True
                if self._axeIsClose is True:
                    hero.attack(self._world.get_unit_by_name("npc_dota_hero_axe").get_id())
                else:
                    self._move_bane(hero)


    def _move_to_secret_shop(self, hero: PlayerHero):
        if not self._axe_in_secret_shop(hero):
            hero.move(-5000, 1800, 0)
        else:
            print("Visited secret shop!")
            self._visitedSecretShop = True
            self._buy_shivas_guard(hero)

    def _buy_shivas_guard(self, hero: PlayerHero):
        hero.buy("item_platemail")

    def _axe_in_secret_shop(self, hero: PlayerHero) -> bool:
        if hero.get_position().x >= -5000 and hero.get_position().x <= -4990:
            if hero.get_position().y >= 1800 and hero.get_position().y <= 1810:
                return True
        return False


    def _move_axe(self, hero: PlayerHero):
        if not self._axe_already_in_position(hero):
            hero.move(-1900, 1400, 0)

    def _move_bane(self, hero: PlayerHero):
        if not self._bane_already_in_position(hero):
            hero.move(-1900, 1250, 0)

    def _axe_already_in_position(self, hero: PlayerHero) -> bool:
        if hero.get_position().x == -1900:
            if hero.get_position().y == 1400:
                if hero.get_position().z == 0:
                    return True
        return False

    def _bane_already_in_position(self, hero: PlayerHero) -> bool:
        if hero.get_position().x == -1900:
            if hero.get_position().y == 1400:
                if hero.get_position().z == 0:
                    return True
        return False