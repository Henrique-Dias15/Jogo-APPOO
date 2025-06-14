import pygame
import random
import math
from utils.settings import *
from entities.experience.experience import Experience
class BaseEnemy(pygame.sprite.Sprite):
    """Base class for all enemies in the game."""

    def __init__(self, player, size, color, speed, hp, shooter, damage, x=None, y=None, screen_width=None, screen_height=None):
        super().__init__()

        # Create enemy sprite with specified size and color
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Reference to player for targeting
        self.player = player

        # Shooter flag
        self.shooter = shooter

        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT

        # Randomize spawn location if not specified
        self.speed = speed
        self.hp = hp
        self.damage = damage

        if x is None or y is None:
            self.spawn_at_screen_edge()
        else:
            self.rect.center = (x, y)


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
            # Check for status effects that prevent movement
        if hasattr(self, 'frozen') and self.frozen:
            return
        
        # Handle charmed enemies (attack other enemies instead)
        if hasattr(self, 'charmed') and self.charmed:
            self.update_charmed_behavior()
            return
        
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

    def can_shoot(self):
        """Check if the enemy can shoot based on cooldown"""
        if not self.shooter:
            return False
        return pygame.time.get_ticks() - self.last_shot > self.projectile_cooldown

    def kill(self, ammount):
        """Handle enemy death"""
        xp = Experience(self.player, self.rect.x, self.rect.y, ammount)
        super().kill()
        return xp
       