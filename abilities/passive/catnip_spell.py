from abilities.base_ability import PassiveAbility
from utils.settings import *

class CatnipSpell(PassiveAbility):
    """Catnip Spell - Increases magical power permanently"""
    def __init__(self):
        # Define projectile modifications for catnip effect
        projectile_mods = {
            'color': (51, 209, 122),  # Plant color
            'visual_effect': 'catnip',
            'particles': 'catnip_trail',  # Not working for now
            'size': (6, 6)  
        }
        
        super().__init__(
            name="Catnip Spell",
            description="Increases magical power permanently",
            stat_name="projectile_damage",
            stat_increase=5,
            projectile_modifications=projectile_mods
        )
        
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add catnip effect to player
        player.has_catnip_spell = True
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.stat_increase += 2
