import pygame
import math
import random
from utils.settings import *

class Enemy(pygame.sprite.Sprite):
    """Base enemy class that can be extended for different enemy types"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, 
                 size=(20, 20), color=RED, speed=None, hp=None):
        super().__init__()
        
        # Create enemy sprite with specified size and color
        self.image = pygame.Surface(size)
        self.image.fill(color)  # Default color is red
        self.rect = self.image.get_rect()
        
        # Reference to player for targeting
        self.player = player
        
        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT
        
        # Randomize spawn location if not specified
        if x is None or y is None:
            self.spawn_at_screen_edge()
        else:
            self.rect.center = (x, y)
        
        # Enemy attributes - use passed values or defaults
        self.speed = speed if speed is not None else ENEMY_SPEED
        self.hp = hp if hp is not None else 20
        self.damage = 10  # Default damage when colliding with player

    def spawn_at_screen_edge(self):
        """Spawn enemy at random edge of screen"""
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            self.rect.midtop = (random.randint(0, self.screen_width), 0)
        elif side == 'bottom':
            self.rect.midbottom = (random.randint(0, self.screen_width), self.screen_height)
        elif side == 'left':
            self.rect.midleft = (0, random.randint(0, self.screen_height))
        else:  # right
            self.rect.midright = (self.screen_width, random.randint(0, self.screen_height))

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