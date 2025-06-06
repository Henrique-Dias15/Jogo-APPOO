import pygame
from abilities.base_ability import PassiveAbility
from utils.settings import *

class FlamingPaws(PassiveAbility):
    """Patas Flamejantes - Adiciona efeito de fogo aos ataques"""
    def __init__(self):        
        # Define projectile modifications for fire effect
        projectile_mods = {
            'color': (255, 69, 0),  # Red-orange for fire
            'visual_effect': 'empowered',
            'particles': 'fire_trail',
            'size': (6, 6)
        }
        
        super().__init__(
            name="Patas Flamejantes",
            description="Ataques causam queimadura nos inimigos e projéteis ficam vermelhos com trilha de fogo",
            stat_name="projectile_damage",
            stat_increase=2,
            projectile_modifications=projectile_mods
        )
        self.burn_duration = 3000  # 3 seconds
        self.burn_damage = 20  # Damage per tick (every 500ms)
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add burn effect to player
        player.has_flaming_paws = True
        player.burn_duration = self.burn_duration
        player.burn_damage = self.burn_damage
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.burn_damage += 5  # Increase burn damage by 5 per upgrade
        self.burn_duration += 500  # Increase duration by 0.5 seconds
