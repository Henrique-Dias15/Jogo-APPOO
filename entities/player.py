import pygame
import math
from utils.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)  # Placeholder green rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player attributes
        self.speed = PLAYER_SPEED
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_MAX_HP
        self.level = 1
        self.exp = 0
        self.projectile_cooldown = 500  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.level_up_callback = None  # Add callback for level up
        self.projectile_damage = 10  # Base projectile damage

    def move(self, keys):
        """Move the player based on keyboard input"""
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
        
        # Diagonal movement normalization
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        self.rect.x += dx
        self.rect.y += dy

    def gain_exp(self, amount):
        """Add experience points and check for level up"""
        self.exp += amount
        if self.exp >= 100:  # Simple level up mechanism
            self.level_up()

    def level_up(self):
        """Handle leveling up logic"""
        self.level += 1
        self.exp -= 100  # Reset exp
        self.hp = min(self.hp + 10, self.max_hp)
        
        # Notify game controller that we've leveled up
        if self.level_up_callback:
            self.level_up_callback()

    def set_level_up_callback(self, callback):
        """Set the function to call when player levels up"""
        self.level_up_callback = callback

    def can_shoot(self):
        """Check if player can shoot a projectile"""
        now = pygame.time.get_ticks()
        return now - self.last_shot > self.projectile_cooldown

    def update(self, keys):
        """Update player state"""
        self.move(keys)