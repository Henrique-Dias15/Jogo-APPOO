import pygame
from abilities.base_ability import PassiveAbility
from entities.player.player import Player

class Tailwind(PassiveAbility):
    """Tailwind - Increases movement speed and firing rate."""
    def __init__(self):
        # Define projectile modifications for tailwind effect
        projectile_mods = {
            'color': (143, 94, 255), # Air color
            'visual_effect': 'tailwind',
            'particles': 'tailwind_trail',
            'size': (5, 5),
            'spritesheet': 'assets/images/abilities/air/Ar.png',
            'sprite_frame_delay': 75,
        }
        
        super().__init__(
            name="Tailwind",
            description="Increases movement speed and firing rate",
            stat_name="speed",                
            stat_increase=0.2,               
            projectile_modifications=projectile_mods
        )
        self.cooldown_reduction = 0.3    
    
    def activate(self, player:Player, **kwargs) -> bool:
        super().activate(player, **kwargs)
        player.has_tailwind = True
        player.projectile_cooldown = int(
            player.projectile_cooldown * (1 - self.cooldown_reduction)
        )
        return True                
    
    def on_upgrade(self):
        super().on_upgrade()
        self.cooldown_reduction = min(self.cooldown_reduction + 0.05, 0.8)