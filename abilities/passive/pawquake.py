from abilities.base_ability import PassiveAbility
from utils.settings import *

class Pawquake(PassiveAbility):
    """Pawquake - Basic attacks have a knockback effect on enemies"""
    def __init__(self):
        # Define projectile modifications for knockback effect
        projectile_mods = {
            'color': (210, 103, 39),  # Earth color
            'visual_effect': 'knockback',
            'particles': 'knockback_trail',  # Placeholder for knockback particles
            'size': (7, 7),
            'spritesheet': 'assets/images/abilities/earth/Terra.png',
            'sprite_frame_delay': 100,
        }
        
        super().__init__(
            name="Pawquake",
            description="Add knockback effect to basic attacks, repelling enemies.",
            stat_name="",
            stat_increase=0,  # No stat increase for this ability
            projectile_modifications=projectile_mods
        )
        self.knockback_distance = 60  # Distance to knock back enemies
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add knockback effect to player
        player.has_pawquake = True
        player.knockback_distance = self.knockback_distance
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.knockback_distance += 10  # Increase knockback distance on upgrade
