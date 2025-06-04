import pygame
import math
import random
from abilities.base_ability import *
from entities.ability_projectile import SpecialProjectile, AbilityProjectile
from utils.settings import *

class CatnipSpell(PassiveAbility):
    """Feitiço de Catnip - Aumenta o poder mágico"""
    def __init__(self):
        super().__init__(
            name="Feitiço de Catnip",
            description="Aumenta o poder mágico permanentemente",
            stat_name="projectile_damage",
            stat_increase=5
        )

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

class PurringShield(BuffAbility):
    """Escudo de Ronronar - Cria uma barreira mágica que da dano a inimigos que encostem"""
    def __init__(self):
        super().__init__(
            name="Escudo de Ronronar",
            description="Cria uma barreira que reflete dano aos inimigos",
            cooldown=8000,
            duration=5000,
            buff_effects={}  # No stat changes, just visual effect
        )
        self.shield_damage = 15
        self.shield_radius = 50
    
    def activate(self, player, **kwargs):
        if not self.can_activate():
            return False
        
        # Add shield attribute to player
        player.has_purring_shield = True
        player.shield_damage = self.shield_damage
        player.shield_radius = self.shield_radius
        
        self.is_active = True
        self.activation_time = pygame.time.get_ticks()
        self.start_cooldown()
        return True
    
    def deactivate(self, player, **kwargs):
        super().deactivate(player, **kwargs)
        # Remove shield
        if hasattr(player, 'has_purring_shield'):
            player.has_purring_shield = False
    
    def on_upgrade(self):
        self.shield_damage += 5
        self.shield_radius += 10

class FelineTeleport(ActiveAbility):
    """Teleporte Felino - Move-se instantaneamente para uma curta distância à frente"""
    def __init__(self):
        super().__init__(
            name="Teleporte Felino",
            description="Teleporta para uma posição segura",
            cooldown=3000,
            auto_trigger=False  # Manual activation when needed
        )
        self.teleport_distance = 100
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate():
            return False
        
        # Calculate safe teleport position away from enemies
        best_position = self.find_safe_position(player, enemies)
        if best_position:
            player.rect.centerx, player.rect.centery = best_position
            self.start_cooldown()
            return True
        return False
    
    def find_safe_position(self, player, enemies):
        """Find a safe position to teleport to"""
        if not enemies:
            # No enemies, teleport forward
            return (
                min(max(player.rect.centerx, 50), player.screen_width - 50),
                min(max(player.rect.centery - self.teleport_distance, 50), player.screen_height - 50)
            )
        
        # Try multiple directions to find safe spot
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(angle)
            new_x = player.rect.centerx + math.cos(rad) * self.teleport_distance
            new_y = player.rect.centery + math.sin(rad) * self.teleport_distance
            
            # Keep within screen bounds
            new_x = min(max(new_x, 50), player.screen_width - 50)
            new_y = min(max(new_y, 50), player.screen_height - 50)
            
            # Check if position is safe (far from enemies)
            safe = True
            for enemy in enemies:
                distance = math.hypot(enemy.rect.centerx - new_x, enemy.rect.centery - new_y)
                if distance < 80:  # Too close to enemy
                    safe = False
                    break
            
            if safe:
                return (new_x, new_y)
        
        return None
    
    def on_upgrade(self):
        self.teleport_distance += 20
        self.cooldown = max(self.cooldown - 200, 1000)

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

class FrozenClaw(PassiveAbility):
    """Garra Gélida - Adiciona efeitos de congelamento aos ataques"""
    def __init__(self):
        super().__init__(
            name="Garra Gélida",
            description="Ataques têm chance de congelar inimigos",
            stat_name="projectile_damage",
            stat_increase=3
        )
        self.freeze_chance = 0.15  # 15% chance
        self.freeze_duration = 2000  # 2 seconds
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add freeze effect to player
        player.has_frozen_claw = True
        player.freeze_chance = self.freeze_chance
        player.freeze_duration = self.freeze_duration
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.freeze_chance += 0.05
