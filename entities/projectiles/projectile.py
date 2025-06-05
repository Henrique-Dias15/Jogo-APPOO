import pygame
import math
from utils.settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, screen_width=None, screen_height=None, speed=7, damage=10):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLUE)  # Blue projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT
        
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
        if (self.rect.right < 0 or self.rect.left > self.screen_width or
            self.rect.bottom < 0 or self.rect.top > self.screen_height):
            self.kill()