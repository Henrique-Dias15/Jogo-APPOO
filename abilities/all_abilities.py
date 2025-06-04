"""
Consolidated import file for all magical cat abilities.
This file imports all abilities from their individual files.
"""

# Passive abilities
from .passive import CatnipSpell, FrozenClaw

# Projectile abilities  
from .projectile import WhiskerBeam, ArcaneFurBall, ElementalTail

# Active abilities
from .active import FelineTeleport, EnchantedGaze, GhostRatSummoning, PurringShield, ReflexAura

# Area effect abilities
from .area_effect import EtherealFishRain, MysticalMeow

# All abilities organized by type (as classes, not instances)
PASSIVE_ABILITIES = [CatnipSpell, FrozenClaw]

PROJECTILE_ABILITIES = [WhiskerBeam, ArcaneFurBall, ElementalTail]

ACTIVE_ABILITIES = [FelineTeleport, EnchantedGaze, GhostRatSummoning, PurringShield, ReflexAura]

AREA_EFFECT_ABILITIES = [EtherealFishRain, MysticalMeow]

# All abilities in one list
ALL_ABILITIES = (
    PASSIVE_ABILITIES + 
    PROJECTILE_ABILITIES + 
    ACTIVE_ABILITIES + 
    AREA_EFFECT_ABILITIES
)

# Abilities by name for easy lookup (creates instances when accessed)
def create_ability_by_name(name):
    """Create an ability instance by class name"""
    ability_classes = {cls.__name__: cls for cls in ALL_ABILITIES}
    if name in ability_classes:
        return ability_classes[name]()
    return None

__all__ = [
    'CatnipSpell', 'FrozenClaw',
    'WhiskerBeam', 'ArcaneFurBall', 'ElementalTail', 
    'FelineTeleport', 'EnchantedGaze', 'GhostRatSummoning', 'PurringShield', 'ReflexAura',
    'EtherealFishRain', 'MysticalMeow',
    'PASSIVE_ABILITIES', 'PROJECTILE_ABILITIES', 'ACTIVE_ABILITIES', 'AREA_EFFECT_ABILITIES',
    'ALL_ABILITIES', 'create_ability_by_name'
]
