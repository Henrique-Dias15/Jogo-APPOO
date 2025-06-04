import pygame
import math
import random
from abilities.base_ability import AreaEffectAbility
from entities.ability_projectile import AbilityProjectile
from utils.settings import CYAN

class EtherealFishRain(AreaEffectAbility):
    """Chuva de Peixes Etéreos - Invoca peixes mágicos que causam dano em área"""
    def __init__(self):
        super().__init__(
            name="Chuva de Peixes Etéreos",
            description="Invoca peixes mágicos que caem do céu",
            cooldown=6000,
            radius=150,
            damage=20
        )
        self.fish_count = 8
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate():
            return False
        
        # Create multiple fish projectiles falling from above
        projectile_manager = kwargs.get('projectile_manager')
        if not projectile_manager:
            return False
        
        for i in range(self.fish_count):
            # Random position around player
            angle = (360 / self.fish_count) * i + random.randint(-15, 15)
            rad = math.radians(angle)
            
            target_x = player.rect.centerx + math.cos(rad) * (self.radius * 0.8)
            target_y = player.rect.centery + math.sin(rad) * (self.radius * 0.8)
            
            # Start fish from above the screen
            start_x = target_x + random.randint(-50, 50)
            start_y = -20
            
            fish = AbilityProjectile(
                start_x, start_y, target_x, target_y,
                speed=4, damage=self.damage,
                size=(10, 6), color=CYAN,
                lifetime=3000
            )
            
            projectile_manager.projectiles.add(fish)
            projectile_manager.all_sprites.add(fish)
        
        self.start_cooldown()
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.fish_count += 2
