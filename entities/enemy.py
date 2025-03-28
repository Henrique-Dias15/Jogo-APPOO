import pygame
import math
from utils.settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, x=None, y=None):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)  # Placeholder red rectangle
        self.rect = self.image.get_rect()
        
        self.player = player
        
        # Randomize spawn location if not specified
        if x is None or y is None:
            self.spawn_at_screen_edge()
        else:
            self.rect.center = (x, y)
        
        self.speed = ENEMY_SPEED
        self.hp = 20

    def spawn_at_screen_edge(self):
        """Spawn enemy at random edge of screen"""
        import random
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            self.rect.midtop = (random.randint(0, SCREEN_WIDTH), 0)
        elif side == 'bottom':
            self.rect.midbottom = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT)
        elif side == 'left':
            self.rect.midleft = (0, random.randint(0, SCREEN_HEIGHT))
        else:  # right
            self.rect.midright = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))

    def update(self, *args, **kwargs):
        """Move enemy towards player, now accepts any arguments"""
        # Calculate direction to player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        
        # Normalize movement
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
        
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def take_damage(self, damage):
        """Handle enemy taking damage"""
        self.hp -= damage
        return self.hp <= 0