import pygame
import math
from entities.enemy import Enemy
from utils.settings import *
from entities.projectile import Projectile

class TriangleEnemy(Enemy):
    """A enemy that keeps a distance from the player and shoots projectiles"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None):
        # Call the parent constructor with custom parameters
        super().__init__(
            player, 
            x, 
            y, 
            screen_width, 
            screen_height, 
            size=(25, 25),  # Medium size
            color=PURPLE,   # Blue color
            speed=3,        # Fast speed
            hp=15           # Less health
        )
        
        # Create a triangle shape
        self.original_image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, BLUE, [(12, 0), (0, 25), (25, 25)])
        self.image = self.original_image

    def update(self, *args, **kwargs):
        """Move enemy towards player and shoot projectiles"""
        # Calculate direction to player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        
        # Normalize movement
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
        
        # Calculate distance to player
        if distance > 500: # If the player is far away, move towards them
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        elif distance < 300: # If the player is too close, move away from them
            self.rect.x -= dx * self.speed
            self.rect.y -= dy * self.speed


