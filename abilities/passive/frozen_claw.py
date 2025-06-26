import pygame
from abilities.base_ability import PassiveAbility
from utils.settings import *
from entities.player.player import Player


class FrozenClaw(PassiveAbility):
    """Frozen Claw - Adds ice effect to attacks, chance to freeze enemies"""
    def __init__(self):
        # Define projectile modifications for ice effect
        projectile_mods = {
            'color': (112, 230, 246),  # Ice color
            'visual_effect': 'frozen',
            'particles': 'ice_trail', # Not working for now
            'size': (7, 7),
            'spritesheet':'assets/images/abilities/ice/Gelo.png',
            'sprite_frame_delay': 100, 
        }
        
        super().__init__(
            name="Frozen Claw",
            description="Attacks have a chance to freeze enemies",
            stat_name="projectile_damage",
            stat_increase=3,
            projectile_modifications=projectile_mods
        )
        self.freeze_chance = 0.15  # 15% chance
        self.freeze_duration = 2000  # 2 seconds
    
    def activate(self, player:Player, **kwargs) -> bool:
        super().activate(player, **kwargs)
        # Add freeze effect to player
        player.has_frozen_claw = True
        player.freeze_chance = self.freeze_chance
        player.freeze_duration = self.freeze_duration
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.freeze_chance += 0.05
