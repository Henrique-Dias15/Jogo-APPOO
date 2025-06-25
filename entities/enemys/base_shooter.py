import pygame
from entities.enemys.base_enemy import BaseEnemy

class BaseShooter(BaseEnemy):
    """Base class for shooter enemies that can shoot projectiles"""
    def __init__(self, player,size, color=None, speed=None, hp=None, damage=None,projectile_damage=None, projectile_cooldown=None,x=None, y=None, screen_width=None, screen_height=None, spritesheet=None, frame_ammount=None, frame_delay=None):
        super().__init__(player,
            size=size, 
            color=color, 
            speed=speed, 
            hp=hp, 
            shooter=True, 
            damage=damage,
            x=x, 
            y=y, 
            screen_width=screen_width, 
            screen_height=screen_height,
            spritesheet=spritesheet,
            frame_ammount=frame_ammount,
            frame_delay=frame_delay,
        )

        self.projectile_damage = projectile_damage
        self.projectile_cooldown = projectile_cooldown
        self.last_shot = pygame.time.get_ticks()