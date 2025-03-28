import pygame
import math
from utils.settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=7, damage=10):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLUE)  # Blue projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx, self.dy = 0, 0
        
        self.damage = damage

    def update(self, *args, **kwargs):
        """Move projectile, now accepts any arguments"""
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove if out of screen
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()