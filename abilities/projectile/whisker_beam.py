import pygame
import math
from abilities.base_ability import ProjectileAbility
from entities.ability_projectile import SpecialProjectile
from utils.settings import YELLOW

class WhiskerBeam(ProjectileAbility):
    """Raio de Bigodes - Dispara feixes mágicos dos bigodes causando dano à distância"""
    def __init__(self):
        super().__init__(
            name="Raio de Bigodes",
            description="Dispara feixes mágicos que atravessam inimigos",
            cooldown=1500,
            projectile_class=SpecialProjectile,
            damage=25,
            speed=8,
            size=(12, 4),
            color=YELLOW
        )
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate() or not enemies:
            return False
        
        # Find closest enemy
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.hypot(
                enemy.rect.centerx - player.rect.centerx,
                enemy.rect.centery - player.rect.centery
            )
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        
        if closest_enemy:
            projectile = SpecialProjectile(
                player.rect.centerx, player.rect.centery,
                closest_enemy.rect.centerx, closest_enemy.rect.centery,
                projectile_type="whisker_beam",
                speed=self.speed, damage=self.damage,
                size=self.size, color=self.color,
                piercing=True, lifetime=2000
            )
            
            # Add to projectile manager if available
            projectile_manager = kwargs.get('projectile_manager')
            if projectile_manager:
                projectile_manager.projectiles.add(projectile)
                projectile_manager.all_sprites.add(projectile)
            
            self.start_cooldown()
            return True
        return False
