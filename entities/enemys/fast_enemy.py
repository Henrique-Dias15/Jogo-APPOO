import pygame
from entities.enemys.enemy import Enemy
from utils.settings import *

class FastEnemy(Enemy):
    """A very fast but weak enemy that does less damage"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None):
        # Call the parent constructor with custom parameters
        super().__init__(
            player, 
            x, 
            y, 
            screen_width, 
            screen_height, 
            size=(15, 15),  # Small size
            color=GREEN,    # Green color
            speed=4,        # Very fast
            hp=10           # Low health
        )
        
        self.damage = 5  # Less damage than normal enemies