import pygame
from entities.enemys.base_enemy import BaseEnemy
from entities.player.player import Player
from typing import Optional, Tuple
class BaseShooter(BaseEnemy):
    """Base class for shooter enemies that can shoot projectiles"""
    def __init__(self, 
        player:Player, 
        size: Tuple[int, int], 
        color: Optional[Tuple[int, int, int]] = None, 
        speed: Optional[float] = None, 
        hp: Optional[int] = None, 
        damage: Optional[float] = None,
        projectile_damage: Optional[float] = None, 
        projectile_cooldown: Optional[int] = None,
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        screen_width: Optional[float] = None, 
        screen_height: Optional[float] = None, 
        spritesheet: Optional[str] = None, 
        frame_ammount: Optional[str] = None, 
        frame_delay: Optional[str] = None
    ) -> None:
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
        self.projectile_modifications = {}
        