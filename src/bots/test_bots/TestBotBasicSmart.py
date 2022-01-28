from typing import Literal, TypedDict, Union, cast
from game.physical_entity import PhysicalEntity
from game.rune import Rune
from game.enums.ability_behavior import AbilityBehavior
from game.courier import Courier
from game.ability import Ability
from game.hero import Hero
from game.position import Position
from game.unit import Unit
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

ARCANE: int = 0
PHASE: int = 1

TOP: int = 0
MID: int = 1
BOT: int = 2

class HeroData(TypedDict):
    boots: Union[Literal[0], Literal[1]]
    lane: Union[Literal[0], Literal[1], Literal[2]]



party: dict[int, dict[str, HeroData]] = {
    RADIANT_TEAM: {
        "npc_dota_hero_abaddon": {
            "boots": ARCANE,
            "lane": TOP,
        },
        "npc_dota_hero_axe": {
            "boots": PHASE,
            "lane": TOP,
        },
        "npc_dota_hero_batrider": {
            "boots": ARCANE,
            "lane": MID,
        },
        "npc_dota_hero_bane": {
            "boots": ARCANE,
            "lane": BOT,
        },
        "npc_dota_hero_disruptor": {
            "boots": ARCANE,
            "lane": BOT,
        },
    },
    DIRE_TEAM: {
        "npc_dota_hero_ancient_apparition": {
            "boots": ARCANE,
            "lane": TOP,
        },
        "npc_dota_hero_alchemist": {
            "boots": PHASE,
            "lane": TOP,
        },
        "npc_dota_hero_dragon_knight": {
            "boots": PHASE,
            "lane": MID,
        },
        "npc_dota_hero_ogre_magi": {
            "boots": ARCANE,
            "lane": BOT,
        },
        "npc_dota_hero_bristleback": {
            "boots": PHASE,
            "lane": BOT,
        },
    },
}

home_position = {
    RADIANT_TEAM: Position(-6774, -6311, 256),
    DIRE_TEAM: Position(6910, 6200, 256),
}

secret_shop_position = {
    RADIANT_TEAM: Position(-5077, 1893, 256),
    DIRE_TEAM: Position(4875, -1286, 256),
}

class TestBotBasicSmart(BaseBot):
    '''
    Tests:
    
    Basic AI.
    - Heroes buy boots of speed and extra town portal scroll at game start.
    - Heroes level up abilities. Will prioritize ultimates.
    - Heroes moves home when hp is less than 30 % of max hp.
    - Heroes moves back to fight when hp is greater than 90 % of max hp.
    - Heroes use town portal scroll to teleport to lane if at home, hp greater than 90 % of max hp and scroll is available.
    - Heroes attack enemy hero if enemy hero has less than 65 % of max hp. Will prioritize casting spells before normal attack.
    - Heroes attempt to get last hits and denies.
    - Heroes "hard"-flee when attacked by tower.
    - Heroes "soft"-flee when attacked by creeps or heroes.
    - Some heroes will buy energy booster using courier which delivers it to the hero to create arcane boots.
    - Heroes with arcane boots will use them when they've lost 175 mana or more.
    - Other heroes will buy blades of attack and chainmail using courier which delivers it to the hero to create phase boots.
    - Heroes with phase boots will use them whenever possible.
    '''
    
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _should_move_home: dict[str, bool]
    _home_position: Position
    _secret_shop_position: Position
    _lane_tower_positions: dict[str, Position]
    _courier_moving_to_secret_shop: dict[str, bool]
    _courier_transferring_items: dict[str, bool]
    _go_aggressive_step1: bool
    _go_aggressive_step2: bool

    def __init__(self, world: World) -> None:
        team: int = world.get_team()

        self._world = world
        self._party = list(party[world.get_team()].keys())
        self._should_move_home = {}
        self._home_position = home_position[team]
        self._secret_shop_position = secret_shop_position[team]
        self._lane_tower_positions = {}
        self._courier_moving_to_secret_shop = {}
        self._courier_transferring_items = {}
        self._go_aggressive_step1 = False
        self._go_aggressive_step2 = False

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes
        for hero in heroes:
            self._should_move_home[hero.get_name()] = False
            self._courier_moving_to_secret_shop[hero.get_name()] = False
            self._courier_transferring_items[hero.get_name()] = False
        self.initialize_lane_tower_positions()

    def initialize_lane_tower_positions(self) -> None:
        for lane_tower_name in [
            "dota_goodguys_tower1_top",
            "dota_goodguys_tower1_mid",
            "dota_goodguys_tower1_bot",
            "dota_goodguys_tower2_top",
            "dota_goodguys_tower2_mid",
            "dota_goodguys_tower2_bot",
            "dota_goodguys_tower3_top",
            "dota_goodguys_tower3_mid",
            "dota_goodguys_tower3_bot",
            "dota_badguys_tower1_top",
            "dota_badguys_tower1_mid",
            "dota_badguys_tower1_bot",
            "dota_badguys_tower2_top",
            "dota_badguys_tower2_mid",
            "dota_badguys_tower2_bot",
            "dota_badguys_tower3_top",
            "dota_badguys_tower3_mid",
            "dota_badguys_tower3_bot",
        ]:
            tower: Union[Unit, None] = self._world.get_unit_by_name(lane_tower_name)
            if tower is not None:
                self._lane_tower_positions[lane_tower_name] = tower.get_position()

    def before_actions(self, game_ticks: int) -> None:
        if (game_ticks % 100 == 0) and self._world.get_team() == 2:
            print("game_ticks:", game_ticks)

        if game_ticks == 1100:
            self._go_aggressive_step1 = True
        elif game_ticks == 1700:
            self._go_aggressive_step2 = True

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        if not hero.is_alive():
            if hero.get_buyback_cooldown_time() == 0 and hero.get_gold() >= hero.get_buyback_cost():
                hero.buyback()
                return
            else:
                hero.courier_move_to_position(*self._home_position)
                return

        if hero.get_stash_items():
            print("Has stash items")
            for item in hero.get_stash_items():
                print(item.get_name())
            hero.courier_retrieve()
            return

        if game_ticks == 1:
            # if self.hero_name_match_any(hero, ["pugna"]):
            #     hero.buy("item_ward_observer")
            # else:
            hero.buy("item_boots")
            return

        if self.buy_tp_scroll(hero):
            return

        # if self.place_observer_ward(hero):
        #     return

        # if self.get_bottle(hero):
        #     return

        # if self.pick_up_rune_with_bottle(hero):
        #     return

        if self.get_better_boots(hero):
            return
        
        if self.use_arcane_boots(hero):
            return

        if self.use_phase_boots(hero):
            return

        self.make_choice(hero)



    def buy_tp_scroll(self, hero: PlayerHero) -> bool:
        if hero.get_gold() >= 100 and hero.is_in_range_of_home_shop() and hero.get_tp_scroll_charges() < 2:
            hero.buy("item_tpscroll")
            return True
        return False

    def pick_up_rune_with_bottle(self, hero: PlayerHero) -> bool:
        bottle_slot: int = self.get_item_slot_by_name(hero, "item_bottle")
        runes: list[Rune] = self._world.get_runes()

        if self.hero_name_match_any(hero, ["pugna"]) \
        and bottle_slot != -1\
        and runes:
            hero.pick_up_rune(runes[0])
            return True

        return False

    def get_bottle(self, hero: PlayerHero) -> bool:
        bottle_slot: int = self.get_item_slot_by_name(hero, "item_bottle")

        if self.hero_name_match_any(hero, ["pugna"]) \
        and bottle_slot == -1:
            courier: Union[PhysicalEntity, None] = self._world.get_entity_by_id(hero.get_courier_id())
            if isinstance(courier, Courier):
                if self.courier_has_bottle(courier):
                    if self._courier_transferring_items[hero.get_name()] == True:
                        return False
                    else:
                        self._courier_transferring_items[hero.get_name()] = True
                        hero.courier_transfer_items()
                        return True
                
                elif hero.get_gold() >= 675:
                    hero.buy("item_bottle")
                    return True

        return False

    def courier_has_bottle(self, courier: Courier) -> bool:
        for item in courier.get_items():
            if item.get_name() == "item_bottle":
                return True
        
        return False

    def place_observer_ward(self, hero: PlayerHero) -> bool:
        ward_slot: int = self.get_item_slot_by_name(hero, "item_ward_observer")

        if ward_slot != -1:
            rune_position: Position = Position(-1629, 1167, 0)

            if self._world.get_distance_between_positions(hero.get_position(), rune_position) < 600:
                runes: list[Rune] = self._world.get_runes()
                if runes:
                    hero.pick_up_rune(runes[0])
                else:
                    hero.use_item(slot=ward_slot, position=rune_position)
            else:
                hero.move(*rune_position)

            return True

        return False

    def get_item_slot_by_name(self, hero: PlayerHero, item_name: str) -> int:
        for item in hero.get_items():
            if item.get_name() == item_name:
                return item.get_slot()

        return -1

    def hero_name_match_any(self, hero: PlayerHero, matches: list[str]) -> bool:
        return hero.get_name() in ["npc_dota_hero_" + match for match in matches]



    def get_top_push_tower_name(self) -> str:
        if self._world.get_team() == RADIANT_TEAM:
            if self._world.get_unit_by_name("dota_goodguys_tower1_top") is not None:
                return "dota_goodguys_tower1_top"
            
            if self._world.get_unit_by_name("dota_goodguys_tower2_top") is not None:
                return "dota_goodguys_tower2_top"

            return "dota_goodguys_tower3_top"
        else:
            if self._world.get_unit_by_name("dota_badguys_tower1_top") is not None:
                return "dota_badguys_tower1_top"
            
            if self._world.get_unit_by_name("dota_badguys_tower2_top") is not None:
                return "dota_badguys_tower2_top"

            return "dota_badguys_tower3_top"

    def get_mid_push_tower_name(self) -> str:
        if self._world.get_team() == RADIANT_TEAM:
            if self._world.get_unit_by_name("dota_goodguys_tower1_mid") is not None:
                return "dota_goodguys_tower1_mid"
            
            if self._world.get_unit_by_name("dota_goodguys_tower2_mid") is not None:
                return "dota_goodguys_tower2_mid"

            return "dota_goodguys_tower3_mid"
        else:
            if self._world.get_unit_by_name("dota_badguys_tower1_mid") is not None:
                return "dota_badguys_tower1_mid"
            
            if self._world.get_unit_by_name("dota_badguys_tower2_mid") is not None:
                return "dota_badguys_tower2_mid"

            return "dota_badguys_tower3_mid"

    def get_bot_push_tower_name(self) -> str:
        if self._world.get_team() == RADIANT_TEAM:
            if self._world.get_unit_by_name("dota_goodguys_tower1_bot") is not None:
                return "dota_goodguys_tower1_bot"
            
            if self._world.get_unit_by_name("dota_goodguys_tower2_bot") is not None:
                return "dota_goodguys_tower2_bot"

            return "dota_goodguys_tower3_bot"
        else:
            if self._world.get_unit_by_name("dota_badguys_tower1_bot") is not None:
                return "dota_badguys_tower1_bot"
            
            if self._world.get_unit_by_name("dota_badguys_tower2_bot") is not None:
                return "dota_badguys_tower2_bot"

            return "dota_badguys_tower3_bot"

    def make_choice(self, hero: PlayerHero) -> None:
        if self.level_up_ability(hero):
            return

        lane = party[self._world.get_team()][hero.get_name()]["lane"]

        if lane == TOP:
            self.push_lane(hero, self.get_top_push_tower_name())
        elif lane == MID:
            self.push_lane(hero, self.get_mid_push_tower_name())
        else:
            self.push_lane(hero, self.get_bot_push_tower_name())

    def level_up_ability(self, hero: PlayerHero) -> bool:
        if hero.get_ability_points() > 0:
            if self.level_up_ultimate(hero):
                return True

            for ability in hero.get_abilities():
                if ability.get_level() < ability.get_max_level() \
                and hero.get_level() >= ability.get_hero_level_required_to_level_up():
                    hero.level_up(ability.get_ability_index())
                    return True

        return False

    def level_up_ultimate(self, hero: PlayerHero) -> bool:
        for ability in hero.get_abilities():
            level_required = ability.get_hero_level_required_to_level_up()
            if (level_required == 6 or level_required == 12 or level_required == 18) \
            and ability.get_level() < ability.get_max_level() \
            and hero.get_level() >= level_required:
                hero.level_up(ability.get_ability_index())
                return True

        return False

    def use_arcane_boots(self, hero: PlayerHero) -> bool:
        if self.has_arcane_boots(hero) \
        and hero.get_max_mana() - hero.get_mana() >= 175:
            for item in hero.get_items():
                if item.get_name() == "item_arcane_boots" \
                and item.get_cooldown_time_remaining() == 0:
                    hero.use_item(item.get_slot())
                    return True

        return False

    def use_phase_boots(self, hero: PlayerHero) -> bool:
        if self.has_phase_boots(hero):
            for item in hero.get_items():
                if item.get_name() == "item_phase_boots" \
                and item.get_cooldown_time_remaining() == 0:
                    hero.use_item(item.get_slot())
                    return True

        return False

    def has_boots(self, hero: PlayerHero) -> bool:
        for item in hero.get_items():
            if item.get_name() == "item_boots":
                return True
        return False

    def get_better_boots(self, hero: PlayerHero) -> bool:
        boots_to_get = party[self._world.get_team()][hero.get_name()]["boots"]
        if boots_to_get == ARCANE:
            if self.has_boots(hero):
                return self.get_arcane_boots(hero)
        
        if boots_to_get == PHASE:
            if self.has_boots(hero):
                return self.get_phase_boots(hero)

        return False

    def get_arcane_boots(self, hero: PlayerHero) -> bool:
        if not self.courier_has_energy_booster(hero) and hero.get_gold() < 800 or self.courier_is_dead(hero):
            return False
        
        if not self.courier_has_energy_booster(hero) and self._world.get_distance_between_positions(self.get_courier_position(hero), self._secret_shop_position) < 500:
            hero.buy("item_energy_booster")
            return True

        if self.courier_has_energy_booster(hero) and not self._courier_transferring_items[hero.get_name()]:
            hero.courier_transfer_items()
            self._courier_transferring_items[hero.get_name()] = True
            self._courier_moving_to_secret_shop[hero.get_name()] = False
            return True

        if not self.courier_has_energy_booster(hero) and not self._courier_moving_to_secret_shop[hero.get_name()]:
            hero.courier_secret_shop()
            self._courier_moving_to_secret_shop[hero.get_name()] = True
            return True

        return False

    def get_phase_boots(self, hero: PlayerHero) -> bool:
        if self.courier_is_dead(hero):
            return False

        if not self.courier_has_blades_of_attack(hero) and hero.get_gold() >= 450:
            hero.buy("item_blades_of_attack")
            return True

        if not self.courier_has_chainmail(hero) and hero.get_gold() >= 550:
            hero.buy("item_chainmail")
            return True

        if self.courier_has_blades_of_attack(hero) and self.courier_has_chainmail(hero) and not self._courier_transferring_items[hero.get_name()]:
            hero.courier_transfer_items()
            self._courier_transferring_items[hero.get_name()] = True
            return True

        return False

    def courier_is_dead(self, hero: PlayerHero) -> bool:
        return self._world.get_entity_by_id(hero.get_courier_id()) is None

    def has_arcane_boots(self, hero: PlayerHero) -> bool:
        for item in hero.get_items():
            if item.get_name() == "item_arcane_boots":
                return True
        return False

    def has_phase_boots(self, hero: PlayerHero) -> bool:
        return "item_phase_boots" in [item.get_name() for item in hero.get_items()]

    def courier_has_energy_booster(self, hero: PlayerHero) -> bool:
        courier = self._world.get_entity_by_id(hero.get_courier_id())

        if isinstance(courier, Courier):
            return "item_energy_booster" in [item.get_name() for item in courier.get_items()]

        return False

    def courier_has_blades_of_attack(self, hero: PlayerHero) -> bool:
        courier = self._world.get_entity_by_id(hero.get_courier_id())

        if isinstance(courier, Courier):
            return "item_blades_of_attack" in [item.get_name() for item in courier.get_items()]

        return False

    def courier_has_chainmail(self, hero: PlayerHero) -> bool:
        courier = self._world.get_entity_by_id(hero.get_courier_id())

        if isinstance(courier, Courier):
            for item in courier.get_items():
                if item.get_name() == "item_chainmail":
                    return True
        return False

    def get_courier_position(self, hero: PlayerHero) -> Position:
        courier = self._world.get_entity_by_id(hero.get_courier_id())
        assert courier is not None
        return courier.get_position()

    def flee_home_or_push_lane(self, hero: PlayerHero, lane_tower_position: Position) -> bool:
        if self.get_unit_hp_percentage(hero) > 90:
            self.should_move_home(hero, False)
            if self.get_distance_to_home(hero) < 2500:
                if hero.use_tp_scroll(lane_tower_position):
                    return True
        elif self.get_unit_hp_percentage(hero) < 30:
            self.should_move_home(hero, True)

        if self.should_move_home(hero):
            if self.get_distance_to_home(hero) > 2500:
                if hero.use_tp_scroll(self._home_position):
                    return True
            hero.move(*self._home_position)
            return True
        
        return False

    def push_lane(self, hero: PlayerHero, lane_tower_name: str) -> None:
        lane_tower_position: Position = self._lane_tower_positions[lane_tower_name]

        if self.flee_home_or_push_lane(hero, lane_tower_position):
            return

        if self.is_near_allied_creeps(hero) and not hero.get_has_tower_aggro():
            enemy_hero_to_attack: Union[Hero, None] = self.get_enemy_hero_to_attack(hero)
            closest_enemy: Union[Unit, None] = self.get_closest_enemy(hero)

            if enemy_hero_to_attack is not None\
            and self.should_attack_hero(hero, enemy_hero_to_attack):
                self.attack_enemy_hero(hero, enemy_hero_to_attack)
                return

            elif self.last_hit_creep(hero):
                return

            elif self.deny_creep(hero):
                return

            elif self._go_aggressive_step2 and enemy_hero_to_attack is not None:
                hero.attack(enemy_hero_to_attack)

            elif self._go_aggressive_step1 and closest_enemy is not None:
                hero.attack(closest_enemy)

            elif hero.get_has_aggro():
                hero.move(*lane_tower_position)

            elif enemy_hero_to_attack is not None:
                hero.attack(enemy_hero_to_attack)

            elif self.should_move_closer_to_allied_creeps(hero):
                self.follow(hero, self.get_closest_allied_creep(hero))
                
            else:
                hero.stop()
        else:
            hero.move(*lane_tower_position)

    def attack_enemy_hero(self, hero: PlayerHero, enemy_hero_to_attack: Hero) -> None:
        hero.attack(enemy_hero_to_attack)
        self.cast_ability(hero, enemy_hero_to_attack)

    def cast_ability(self, hero: PlayerHero, enemy_hero_to_attack: Hero) -> bool:
        ability: Union[Ability, None] = self.get_ability_to_cast(hero)

        if ability is not None:
            behavior: int = ability.get_behavior()

            if behavior & AbilityBehavior.UNIT_TARGET.value:
                hero.cast_target_unit(ability.get_ability_index(), enemy_hero_to_attack)
                return True
            elif behavior & AbilityBehavior.NO_TARGET.value:
                hero.cast_no_target(ability.get_ability_index())
                return True
            elif behavior & AbilityBehavior.AOE.value:
                hero.cast_target_area(ability.get_ability_index(), enemy_hero_to_attack.get_position())
                return True
            elif behavior & AbilityBehavior.POINT.value:
                hero.cast_target_point(ability.get_ability_index(), enemy_hero_to_attack.get_position())
                return True
            elif behavior & AbilityBehavior.CHANNELLED.value:
                hero.cast(
                    ability_index=ability.get_ability_index(),
                    target=enemy_hero_to_attack,
                    position=enemy_hero_to_attack.get_position(),
                )
                return True

        return False

    def last_hit_creep(self, hero: PlayerHero) -> bool:
        creep_to_last_hit: Union[Unit, None] = self.get_creep_to_last_hit(hero)
        
        if creep_to_last_hit is not None:
            hero.attack(creep_to_last_hit)
            return True

        return False

    def deny_creep(self, hero: PlayerHero) -> bool:
        creep_to_deny: Union[Unit, None] = self.get_creep_to_deny(hero)

        if creep_to_deny is not None:
            hero.attack(creep_to_deny)
            return True
        
        return False

    def get_distance_to_home(self, hero: PlayerHero) -> float:
        return self._world.get_distance_between_positions(hero.get_position(), self._home_position)

    def should_move_home(self, hero: PlayerHero, new_value: Union[bool, None] = None) -> Union[bool, None]:
        if new_value is None:
            return self._should_move_home[hero.get_name()]
        
        self._should_move_home[hero.get_name()] = new_value

    def should_attack_hero(self, hero: PlayerHero, enemy_hero_to_attack: Hero) -> bool:
        # todo check ability cooldowns & level
        return self.get_unit_hp_percentage(enemy_hero_to_attack) < 65 or\
                self.get_unit_mana_percentage(hero) > 95 or\
                (self._go_aggressive_step1 and self.get_unit_mana_percentage(hero) > 80) or\
                (self._go_aggressive_step2 and self.get_unit_mana_percentage(hero) > 70)

    def get_unit_hp_percentage(self, unit: Unit) -> float:
        '''Returns value in range 0-100.'''
        return unit.get_health() / unit.get_max_health() * 100

    def get_unit_mana_percentage(self, unit: Unit) -> float:
        '''Returns value in range 0-100.'''
        return unit.get_mana() / unit.get_max_mana() * 100

    def follow(self, hero: PlayerHero, to_follow: Unit) -> None:
        hero.move(*to_follow.get_position())

    def get_ability_to_cast(self, hero: PlayerHero) -> Union[Ability, None]:
        for i in range(4):
            ability: Ability = hero.get_abilities()[i]
            behavior: int = ability.get_behavior()
            if ability.get_level() > 0 \
            and ability.get_cooldown_time_remaining() == 0 \
            and (
                behavior & AbilityBehavior.UNIT_TARGET.value or\
                behavior & AbilityBehavior.NO_TARGET.value or\
                behavior & AbilityBehavior.AOE.value or\
                behavior & AbilityBehavior.POINT.value or\
                behavior & AbilityBehavior.CHANNELLED.value
            ) \
            and ability.get_mana_cost() <= hero.get_mana():
                return ability

    def should_move_closer_to_allied_creeps(self, hero: PlayerHero) -> bool:
        return not self._world.get_enemies_in_range_of(hero, 575)

    def get_creep_to_deny(self, hero: PlayerHero) -> Union[Unit, None]:
        closest_allied_creeps = self.get_closest_allied_creeps(hero)

        closest_allied_creeps.sort(key=lambda creep: self._world.get_distance_between_units(hero, creep))

        for creep in closest_allied_creeps:
            if creep.is_deniable() and creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def get_closest_allied_creeps(self, hero: PlayerHero) -> list[Unit]:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_allied_creeps: list[Unit] = []

        for creep in creeps:
            if self._world.get_distance_between_units(hero, creep) < 600:
                close_allied_creeps.append(creep)

        return close_allied_creeps

    def get_enemy_hero_to_attack(self, hero: PlayerHero) -> Union[Hero, None]:
        enemy_heroes: list[Hero] = self.get_closest_enemy_heroes(hero)
        heroes_with_hp: dict[Hero, int] = {}

        for enemy_hero in enemy_heroes:
            heroes_with_hp[enemy_hero] = enemy_hero.get_health()

        if len(heroes_with_hp) == 0:
            return

        return min(heroes_with_hp.keys(), key=(lambda enemy_hero: heroes_with_hp[enemy_hero]))
        
    def get_closest_enemy_heroes(self, hero: PlayerHero) -> list[Hero]:
        enemy_heroes: list[Hero] = self._world.get_enemy_heroes_of(hero)
        close_enemy_heroes: list[Hero] = []

        for enemy_hero in enemy_heroes:
            if self._world.get_distance_between_units(hero, enemy_hero) < 1250:
                close_enemy_heroes.append(enemy_hero)

        return close_enemy_heroes

    def get_creep_to_last_hit(self, hero: PlayerHero) -> Union[Unit, None]:
        closest_enemy_creeps = self.get_closest_enemy_creeps(hero)

        for creep in closest_enemy_creeps:
            if creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def is_near_allied_creeps(self, hero: PlayerHero) -> bool:
        allied_creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_allies: list[Unit] = self._world.get_allies_in_range_of(hero, 750)

        for ally in close_allies:
            if ally in allied_creeps:
                return True
        return False

    def get_closest_enemy(self, hero: PlayerHero) -> Union[Unit, None]:
        enemies: list[Unit] = self.get_closest_enemy_creeps(hero) + cast(list[Unit], self.get_closest_enemy_heroes(hero))
        enemies_with_distance_to_hero: dict[Unit, float] = {}

        for enemy in enemies:
            enemies_with_distance_to_hero[enemy] = self._world.get_distance_between_units(hero, enemy)

        return min(enemies_with_distance_to_hero.keys(), key=(lambda allied_creep: enemies_with_distance_to_hero[allied_creep]), default=None)

    def get_closest_enemy_creeps(self, hero: PlayerHero) -> list[Unit]:
        creeps: list[Unit] = self._world.get_enemy_creeps_of(hero)
        close_enemy_creeps: list[Unit] = []

        for creep in creeps:
            if self._world.get_distance_between_units(hero, creep) < 500 or self._world.get_distance_between_units(hero, creep) < hero.get_attack_range():
                close_enemy_creeps.append(creep)

        return close_enemy_creeps

    def get_closest_allied_creep(self, hero: PlayerHero) -> Unit:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        creeps_with_distance_to_hero: dict[Unit, float] = {}

        for allied_creep in creeps:
            if allied_creep.get_name() == "npc_dota_ward_base":
                continue
            creeps_with_distance_to_hero[allied_creep] = self._world.get_distance_between_units(hero, allied_creep)

        return min(creeps_with_distance_to_hero.keys(), key=(lambda allied_creep: creeps_with_distance_to_hero[allied_creep]))
