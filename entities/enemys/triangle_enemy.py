import pygame
import math
from entities.enemys.base_shooter import BaseShooter
from utils.settings import *
from entities.projectiles.projectile import Projectile
from entities.player.player import Player
from typing import Optional, Tuple
from entities.experience.experience import Experience

class TriangleEnemy(BaseShooter):
    """A enemy that keeps a distance from the player and shoots projectiles"""
    def __init__(self, 
        player: Player, 
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        screen_width: Optional[float] = None, 
        screen_height: Optional[float] = None, 
        speed: Optional[float] = TRIANGLE_ENEMY_SPEED, 
        hp: Optional[int] = TRIANGLE_ENEMY_HP, 
        damage:Optional[float] = TRIANGLE_ENEMY_DAMAGE, 
        projectile_cooldown: Optional[int] = TRIANGLE_ENEMY_PROJECTILE_COOLDOWN, 
        projectile_damage: Optional[float] = TRIANGLE_ENEMY_PROJECTILE_DAMAGE
        ) -> None:
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
            spritesheet='assets/images/enemys/bottle_spray/Pshpsh.png',
            frame_ammount=2,  # Number of frames in the sprite sheet
            frame_delay=200,
        )
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.projectile_modifications = {
            'spritesheet': 'assets/images/enemys/bottle_spray/Projetil.png',
            'sprite_frame_delay': 150,
        }

    def update(self, *args, **kwargs) -> None:
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

    def kill(self) -> Experience:
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(20)