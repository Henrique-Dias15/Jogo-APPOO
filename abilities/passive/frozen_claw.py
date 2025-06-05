import pygame
from abilities.base_ability import PassiveAbility
from utils.settings import *

class FrozenClaw(PassiveAbility):
    """Garra Gélida - Adiciona efeitos de congelamento aos ataques"""
    def __init__(self):
        # Define projectile modifications for ice effect
        projectile_mods = {
            'color': (135, 206, 250),  # Light blue for ice
            'visual_effect': 'frozen',
            'particles': 'ice_trail',
            'size': (7, 7)  # Slightly larger
        }
        
        super().__init__(
            name="Garra Gélida",
            description="Ataques têm chance de congelar inimigos e projéteis ficam azul gelo",
            stat_name="projectile_damage",
            stat_increase=3,
            projectile_modifications=projectile_mods
        )
        self.freeze_chance = 0.15  # 15% chance
        self.freeze_duration = 2000  # 2 seconds
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add freeze effect to player
        player.has_frozen_claw = True
        player.freeze_chance = self.freeze_chance
        player.freeze_duration = self.freeze_duration
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.freeze_chance += 0.05
