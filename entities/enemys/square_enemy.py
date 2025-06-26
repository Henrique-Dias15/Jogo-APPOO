import pygame
from entities.enemys.base_enemy import BaseEnemy
from utils.settings import *
from entities.player.player import Player
from typing import Optional, Tuple
from entities.experience.experience import Experience
class SquareEnemy(BaseEnemy):
    """A larger, slower enemy with more health than the base enemy"""
    def __init__(self, 
        player:Player, 
        x :Optional[float] = None, 
        y :Optional[float] = None, 
        screen_width: Optional[float] = None, 
        screen_height: Optional[float] = None, 
        speed: Optional[float] = SQUARE_ENEMY_SPEED, 
        hp: Optional[float] = SQUARE_ENEMY_HP, 
        shooter: Optional[bool] = False, 
        damage: Optional[float] = SQUARE_ENEMY_DAMAGE
    ) -> None:
        # Call the parent constructor with custom parameters
        super().__init__(
            player,
            size=(130, 130),  # Larger size
            color=RED,      # Red color
            speed=speed,      # Slower speed
            hp=hp,          # More health
            shooter=shooter,
            damage=damage,
            x=x,
            y=y,
            screen_width=screen_width,
            screen_height=screen_height,
            spritesheet='assets/images/enemys/dog/Cachorro.png',
            frame_ammount=2,
            frame_delay=200
        )

    def kill(self) -> Experience:
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(15)
    
    def update(self, *args, **kwargs) -> None:
        """Update the enemy's position and animation"""
        super().update()
        
        self.update_animation_turning()