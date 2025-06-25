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
            size=(125, 125),  # Medium size
            color=BLUE,   # Blue color
            speed=speed,        # Fast speed
            hp=hp,
            damage=damage,
            projectile_cooldown=projectile_cooldown,
            projectile_damage=projectile_damage,
            spritesheet='assets/images/bottle_spray/Pshpsh.png',
            frame_ammount=2,  # Number of frames in the sprite sheet
            frame_delay=200,
        )
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

    def update(self, *args, **kwargs):
        """Move enemy towards player and shoot projectiles"""
        # Calculate direction to player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        
        # Normalize movement
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance

        self.angle = math.degrees(math.atan2(-dy, dx))  # Adjust angle for pygame coordinate system

        # Calculate distance to player
        if distance > 500: # If the player is far away, move towards them
            self.pos_x += dx * self.speed
            self.pos_y += dy * self.speed
            self.shooter = False
            self.has_animation = False
        elif distance < 300: # If the player is too close, move away from them
            self.pos_x -= dx * self.speed
            self.pos_y -= dy * self.speed
            self.shooter = False
            self.has_animation = False
        else:  # If the player is at a medium distance, shoot projectiles
            self.shooter = True
            self.has_animation = True

        self.pos_x = max(0, min(self.pos_x, self.screen_width - self.rect.width))
        self.pos_y = max(0, min(self.pos_y, self.screen_height - self.rect.height))

        # Atualize o rect a partir da posição real
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        self.update_animation_turning()

    def kill(self):
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(20)