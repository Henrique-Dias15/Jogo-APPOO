from abilities.base_ability import PassiveAbility
from utils.settings import *

class StaticFur(PassiveAbility):
    """Static Fur - Basic attacks can jump to nearby enemies."""
    def __init__(self):
        # Define projectile modifications for static fur effect
        projectile_mods = {
            'color':  (242, 255, 61),  # Electric color
            'visual_effect': 'static_jump',
            'particles': 'static_trail',  # Placeholder for static particles
            'size': (6, 6),
            'spritesheet': 'assets/images/lightning/Raio.png',  # Placeholder for static fur spritesheet
            'sprite_frame_delay': 150,  # Frame rate for static fur animation
        }
        
        super().__init__(
            name="Static Fur",
            description="Basic attacks can jump to nearby enemies.",
            stat_name="",
            stat_increase=0,  # No stat increase for this ability
            projectile_modifications=projectile_mods
        )
        self.enemies_jump = 2  # Number of enemies to jump to

    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        player.has_static_fur = True
        player.static_max_jumps = self.enemies_jump
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.enemies_jump += 1  # Increase number of enemies to jump to on upgrade