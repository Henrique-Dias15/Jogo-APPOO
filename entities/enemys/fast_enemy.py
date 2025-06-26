import pygame
from entities.enemys.base_enemy import BaseEnemy
from utils.settings import *
from entities.player.player import Player
from typing import Optional, Tuple
from entities.experience.experience import Experience
class FastEnemy(BaseEnemy):
    """A very fast but weak enemy that does less damage"""
    def __init__(self, 
        player: Player, 
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        screen_width: Optional[float] = None, 
        screen_height: Optional[float] = None, 
        speed: Optional[float] = FAST_ENEMY_SPEED, 
        hp: Optional[int] = FAST_ENEMY_HP, 
        shooter: Optional[bool] = False, 
        damage: Optional[float] = FAST_ENEMY_DAMAGE
    ):
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

    def kill(self) -> Experience:
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(5)
    
    def update(self, *args, **kwargs) -> None:
        """Update the enemy's position and state"""
        result = super().update(*args, **kwargs)
        self.update_animation_turning_rotation()