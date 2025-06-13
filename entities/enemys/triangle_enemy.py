import pygame
import math
from entities.enemys.base_shooter import BaseShooter
from utils.settings import *
from entities.projectiles.projectile import Projectile

class TriangleEnemy(BaseShooter):
    """A enemy that keeps a distance from the player and shoots projectiles"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, speed=TRIANGLE_ENEMY_SPEED, hp=TRIANGLE_ENEMY_HP, shooter=True, damage=TRIANGLE_ENEMY_DAMAGE, projectile_cooldown=TRIANGLE_ENEMY_PROJECTILE_COOLDOWN, projectile_damage=TRIANGLE_ENEMY_PROJECTILE_DAMAGE):
        # Call the parent constructor with custom parameters
        super().__init__(
            player=player,
            x=x,
            y=y,
            screen_width=screen_width,
            screen_height=screen_height,
            size=(25, 25),  # Medium size
            color=BLUE,   # Blue color
            speed=speed,        # Fast speed
            hp=hp,
            damage=damage,
            projectile_cooldown=projectile_cooldown,
            projectile_damage=projectile_damage
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
            self.shooter = False
        elif distance < 300: # If the player is too close, move away from them
            self.rect.x -= dx * self.speed
            self.rect.y -= dy * self.speed
            self.shooter = False
        else:  # If the player is at a medium distance, shoot projectiles
            self.shooter = True
