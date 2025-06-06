import pygame
import math
from utils.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width=None, screen_height=None):
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
        
        # Ability-related attributes
        self.has_frozen_claw = False
        self.freeze_chance = 0
        self.freeze_duration = 0
        self.has_flaming_paws = False
        self.burn_duration = 0
        self.burn_damage = 0
        
        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT

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

        # Update position
        self.rect.x += dx
        self.rect.y += dy
        
        # Apply boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

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
        self.draw_shield_effect()
    
    def draw_shield_effect(self):
        """Draw purring shield visual effect if active."""
        if hasattr(self, 'has_purring_shield') and self.has_purring_shield:
            # Create a larger surface for the shield effect
            shield_surface = pygame.Surface((self.shield_radius * 2, self.shield_radius * 2), pygame.SRCALPHA)
            center = (self.shield_radius, self.shield_radius)
            
            # Draw shield ring
            pygame.draw.circle(shield_surface, (0, 255, 255, 60), center, self.shield_radius, 3)
            pygame.draw.circle(shield_surface, (0, 255, 255, 30), center, self.shield_radius - 10, 2)
            
            # Blit shield to main surface (this would normally be done in render)
            # For now, we'll modify the player image to show shield status
            if self.shield_radius > 0:
                # Create a temporary visual indicator by adding a blue border
                temp_image = pygame.Surface((35, 35), pygame.SRCALPHA)
                temp_image.fill((0, 0, 0, 0))
                pygame.draw.rect(temp_image, (0, 255, 255), (0, 0, 35, 35), 2)
                temp_image.blit(self.image, (2, 2))
                self.image = temp_image