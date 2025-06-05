from abilities.base_ability import PassiveAbility
from utils.settings import *

class CatnipSpell(PassiveAbility):
    """Feitiço de Catnip - Aumenta o poder mágico"""
    def __init__(self):
        # Define projectile modifications for catnip effect
        projectile_mods = {
            'color': (130, 167, 145),  # Green color for catnip
            'visual_effect': 'catnip',
            'particles': 'catnip_trail',  # Not working for now
            'size': (6, 6)  
        }
        
        super().__init__(
            name="Feitiço de Catnip",
            description="Aumenta o poder mágico permanentemente",
            stat_name="projectile_damage",
            stat_increase=5,
            projectile_modifications=projectile_mods
        )
        
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add catnip effect to player
        player.has_catnip_spell = True
        player.catnip_spell_damage_increase = self.stat_increase
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.stat_increase += 2
