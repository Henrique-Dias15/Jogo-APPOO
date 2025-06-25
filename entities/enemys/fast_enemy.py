import pygame
from entities.enemys.base_enemy import BaseEnemy
from utils.settings import *

class FastEnemy(BaseEnemy):
    """A very fast but weak enemy that does less damage"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, speed=FAST_ENEMY_SPEED, hp=FAST_ENEMY_HP, shooter=False, damage=FAST_ENEMY_DAMAGE):
        # Call the parent constructor with custom parameters
        super().__init__(
            player,
            size=(100, 100),  # Small size
            color=GREEN,     # Green color
            speed=speed,
            hp=hp,
            shooter=shooter,
            damage=damage,
            x=x,
            y=y,
            screen_width=screen_width,
            screen_height=screen_height,
            spritesheet='assets/images/enemys/bird/Pombo.png',
            frame_ammount=2,  # Number of frames in the sprite sheet
            frame_delay=100
        )

    def kill(self):
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(5)
    
    def update(self, *args, **kwargs):
        """Update the enemy's position and state"""
        result = super().update(*args, **kwargs)
        self.update_animation_turning_rotation()