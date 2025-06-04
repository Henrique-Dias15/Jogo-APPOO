import pygame
import random
from abilities.base_ability import ProjectileAbility
from entities.ability_projectile import SpecialProjectile
from utils.settings import PURPLE

class ArcaneFurBall(ProjectileAbility):
    """Bola de Pêlo Arcana - Lança uma esfera mágica que explode ao contato"""
    def __init__(self):
        super().__init__(
            name="Bola de Pêlo Arcana",
            description="Lança esferas explosivas de pelos mágicos",
            cooldown=2500,
            projectile_class=SpecialProjectile,
            damage=35,
            speed=6,
            size=(16, 16),
            color=PURPLE
        )
        self.explosion_radius = 60
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate() or not enemies:
            return False
        
        # Target random enemy
        target_enemy = random.choice(list(enemies))
        
        projectile = SpecialProjectile(
            player.rect.centerx, player.rect.centery,
            target_enemy.rect.centerx, target_enemy.rect.centery,
            projectile_type="fur_ball",
            speed=self.speed, damage=self.damage,
            size=self.size, color=self.color,
            explosion_radius=self.explosion_radius
        )
        
        # Add to projectile manager
        projectile_manager = kwargs.get('projectile_manager')
        if projectile_manager:
            projectile_manager.projectiles.add(projectile)
            projectile_manager.all_sprites.add(projectile)
        
        self.start_cooldown()
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.explosion_radius += 15
