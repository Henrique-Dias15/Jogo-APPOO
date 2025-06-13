import pygame
from entities.enemys.base_enemy import BaseEnemy
from utils.settings import *

class SquareEnemy(BaseEnemy):
    """A larger, slower enemy with more health than the base enemy"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, speed=SQUARE_ENEMY_SPEED, hp=SQUARE_ENEMY_HP, shooter=False, damage=SQUARE_ENEMY_DAMAGE):
        # Call the parent constructor with custom parameters
        super().__init__(
            player,
            size=(40, 40),  # Larger size
            color=RED,      # Red color
            speed=speed,      # Slower speed
            hp=hp,          # More health
            shooter=shooter,
            damage=damage,
            x=x,
            y=y,
            screen_width=screen_width,
            screen_height=screen_height
        )