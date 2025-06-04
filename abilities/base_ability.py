import pygame
import math
from abc import ABC, abstractmethod
from utils.settings import *

class BaseAbility(ABC):
    """
    Abstract base class for all abilities in the game.
    Provides common functionality and enforces implementation of key methods.
    """
    def __init__(self, name, description, cooldown, level=1, max_level=5):
        self.name = name
        self.description = description
        self.base_cooldown = cooldown
        self.cooldown = cooldown
        self.level = level
        self.max_level = max_level
        self.last_used = 0
        self.is_active = False
        self.duration = 0  # For abilities with duration
        self.activation_time = 0
        
    @abstractmethod
    def activate(self, player, enemies=None, projectiles=None, **kwargs):
        """
        Activate the ability. Must be implemented by subclasses.
        """
        pass
    
    def can_activate(self):
        """
        Check if the ability can be activated (cooldown check).
        """
        current_time = pygame.time.get_ticks()
        return current_time - self.last_used >= self.cooldown
    
    def start_cooldown(self):
        """
        Start the ability cooldown.
        """
        self.last_used = pygame.time.get_ticks()
    
    def upgrade(self):
        """
        Upgrade the ability to the next level.
        """
        if self.level < self.max_level:
            self.level += 1
            self.on_upgrade()
            return True
        return False
    
    def on_upgrade(self):
        """
        Override this method to define what happens when ability is upgraded.
        """
        pass
    
    def update(self, dt, player, enemies=None, projectiles=None, **kwargs):
        """
        Update the ability state. Called every frame.
        Override for abilities that need continuous updates.
        """
        # Check if timed ability should deactivate
        if self.is_active and self.duration > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.activation_time >= self.duration:
                self.deactivate(player, **kwargs)
    
    def deactivate(self, player, **kwargs):
        """
        Deactivate the ability. Override for abilities with duration.
        """
        self.is_active = False


class PassiveAbility(BaseAbility):
    """
    Base class for passive abilities that provide permanent stat boosts.
    """
    def __init__(self, name, description, stat_name, stat_increase):
        super().__init__(name, description, cooldown=0)  # No cooldown for passive abilities
        self.stat_name = stat_name
        self.base_stat_increase = stat_increase
        self.stat_increase = stat_increase
    
    def activate(self, player, **kwargs):
        """
        Apply the passive effect to the player.
        """
        self.apply_stat_boost(player)
        return True
    
    def apply_stat_boost(self, player):
        """
        Apply the stat boost to the player.
        """
        if hasattr(player, self.stat_name):
            current_value = getattr(player, self.stat_name)
            setattr(player, self.stat_name, current_value + self.stat_increase)
    
    def on_upgrade(self):
        """
        Increase the stat boost when upgraded.
        """
        self.stat_increase = self.base_stat_increase * self.level


class ActiveAbility(BaseAbility):
    """
    Base class for active abilities that are triggered automatically or manually.
    """
    def __init__(self, name, description, cooldown, auto_trigger=True):
        super().__init__(name, description, cooldown)
        self.auto_trigger = auto_trigger
    
    def should_auto_trigger(self, player, enemies=None, **kwargs):
        """
        Determine if the ability should auto-trigger.
        Override for custom trigger conditions.
        """
        return self.auto_trigger and self.can_activate() and enemies


class ProjectileAbility(ActiveAbility):
    """
    Base class for abilities that create projectiles.
    """
    def __init__(self, name, description, cooldown, projectile_class, 
                 damage, speed=5, size=(8, 8), color=BLUE, auto_trigger=True):
        super().__init__(name, description, cooldown, auto_trigger)
        self.projectile_class = projectile_class
        self.base_damage = damage
        self.damage = damage
        self.speed = speed
        self.size = size
        self.color = color
    
    def create_projectile(self, start_x, start_y, target_x, target_y, **kwargs):
        """
        Create a projectile instance.
        """
        from entities.ability_projectile import AbilityProjectile
        return AbilityProjectile(
            start_x, start_y, target_x, target_y,
            speed=self.speed, damage=self.damage,
            size=self.size, color=self.color, **kwargs
        )
    
    def on_upgrade(self):
        """
        Increase damage and reduce cooldown when upgraded.
        """
        self.damage = self.base_damage * self.level
        self.cooldown = max(self.base_cooldown - (self.level - 1) * 100, self.base_cooldown * 0.3)


class AreaEffectAbility(ActiveAbility):
    """
    Base class for abilities that affect an area.
    """
    def __init__(self, name, description, cooldown, radius, damage, auto_trigger=True):
        super().__init__(name, description, cooldown, auto_trigger)
        self.base_radius = radius
        self.radius = radius
        self.base_damage = damage
        self.damage = damage
    
    def get_enemies_in_range(self, center_x, center_y, enemies):
        """
        Get all enemies within the ability's radius.
        """
        enemies_in_range = []
        for enemy in enemies:
            distance = math.hypot(
                enemy.rect.centerx - center_x,
                enemy.rect.centery - center_y
            )
            if distance <= self.radius:
                enemies_in_range.append(enemy)
        return enemies_in_range
    
    def on_upgrade(self):
        """
        Increase radius and damage when upgraded.
        """
        self.radius = self.base_radius + (self.level - 1) * 20
        self.damage = self.base_damage + (self.level - 1) * 10


class BuffAbility(BaseAbility):
    """
    Base class for abilities that temporarily buff the player.
    """
    def __init__(self, name, description, cooldown, duration, buff_effects):
        super().__init__(name, description, cooldown)
        self.duration = duration
        self.buff_effects = buff_effects  # Dict of stat_name: multiplier
        self.original_stats = {}
    
    def activate(self, player, **kwargs):
        """
        Apply temporary buffs to the player.
        """
        if not self.can_activate():
            return False
        
        # Store original stats
        for stat_name in self.buff_effects:
            if hasattr(player, stat_name):
                self.original_stats[stat_name] = getattr(player, stat_name)
                # Apply buff
                new_value = self.original_stats[stat_name] * self.buff_effects[stat_name]
                setattr(player, stat_name, new_value)
        
        self.is_active = True
        self.activation_time = pygame.time.get_ticks()
        self.start_cooldown()
        return True
    
    def deactivate(self, player, **kwargs):
        """
        Remove buffs and restore original stats.
        """
        # Restore original stats
        for stat_name, original_value in self.original_stats.items():
            if hasattr(player, stat_name):
                setattr(player, stat_name, original_value)
        
        super().deactivate(player, **kwargs)
        self.original_stats.clear()