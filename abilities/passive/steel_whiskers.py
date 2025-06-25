from abilities.base_ability import PassiveAbility
from utils.settings import *

class SteelWhiskers(PassiveAbility):
    """Steel Whiskers - Basic attacks can pierce through enemies"""
    def __init__(self):
        # Define projectile modifications for piercing effect
        projectile_mods = {
            'color': (192, 192, 249),  # Metal color
            'visual_effect': 'piercing',
            'particles': 'piercing_trail',  # Placeholder for piercing particles
            'size': (8, 8),
            'spritesheet': 'assets/images/abilities/metal/Metal.png',
            'sprite_frame_delay': 50,
        }
        
        super().__init__(
            name="Steel Whiskers",
            description="Basic attacks can pierce through enemies.",
            stat_name="",
            stat_increase=0,  # No stat increase for this ability
            projectile_modifications=projectile_mods
        )
        self.max_pierces = 2  # Number of enemies to pierce through
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add piercing effect to player
        player.has_steel_whiskers = True
        player.piercing_count = self.max_pierces
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.max_pierces += 1  # Increase number of pierces on upgrade
