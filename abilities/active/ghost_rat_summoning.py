import pygame
import math
from abilities.base_ability import ActiveAbility
from entities.projectiles.ability_projectile import AbilityProjectile
from utils.settings import GREY

class GhostRatSummoning(ActiveAbility):
    """Invocação de Ratos Fantasmas - Invoca ratos mágicos que perseguem e atacam inimigos"""
    def __init__(self):
        super().__init__(
            name="Invocação de Ratos Fantasmas",
            description="Invoca ratos espectrais que caçam inimigos",
            cooldown=7000
        )
        self.rat_count = 3
        self.rat_lifetime = 8000  # 8 seconds
        self.rat_damage = 15
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate():
            return False
        
        projectile_manager = kwargs.get('projectile_manager')
        if not projectile_manager:
            return False
        
        # Create ghost rats that home in on enemies
        for i in range(self.rat_count):
            # Spawn rats in a circle around player
            angle = (360 / self.rat_count) * i
            rad = math.radians(angle)
            
            start_x = player.rect.centerx + math.cos(rad) * 40
            start_y = player.rect.centery + math.sin(rad) * 40
            
            # Target closest enemy or random direction
            target_x, target_y = player.rect.centerx, player.rect.centery
            if enemies:
                closest_enemy = min(enemies, key=lambda e: math.hypot(
                    e.rect.centerx - start_x, e.rect.centery - start_y
                ))
                target_x, target_y = closest_enemy.rect.centerx, closest_enemy.rect.centery
            
            ghost_rat = AbilityProjectile(
                start_x, start_y, target_x, target_y,
                speed=3, damage=self.rat_damage,
                size=(8, 8), color=GREY,
                homing=True, lifetime=self.rat_lifetime
            )
            
            projectile_manager.projectiles.add(ghost_rat)
            projectile_manager.all_sprites.add(ghost_rat)
        
        self.start_cooldown()
        return True
    
    def on_upgrade(self):
        self.rat_count += 1
        self.rat_damage += 5
