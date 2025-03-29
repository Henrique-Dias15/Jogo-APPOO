import pygame
from entities.enemy import Enemy
from utils.settings import *

class SquareEnemy(Enemy):
    """A larger, slower enemy with more health than the base enemy"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None):
        # Call the parent constructor with custom parameters
        super().__init__(
            player, 
            x, 
            y, 
            screen_width, 
            screen_height, 
            size=(40, 40),  # Larger size
            color=RED,      # Red color
            speed=1.5,      # Slower speed
            hp=40           # More health
        )