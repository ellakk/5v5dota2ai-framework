from game.post_data_interfaces.IPosition import IPosition
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class IUnit(IPhysicalEntity):
    dominated: bool
    mana: int
    disarmed: bool
    maxHealth: int
    health: int
    blind: bool
    isAttacking: bool
    team: int
    maxMana: int
    level: int
    attackRange: int
    attackDamage: int
    attackTarget: str
    alive: bool
    forwardVector: IPosition
    rooted: bool
    name: str
    deniable: bool
    magicimmune: bool