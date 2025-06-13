import pygame
import math
from utils.settings import *

class AbilityProjectile(pygame.sprite.Sprite):
    """
    Projectile class specifically for abilities, with more customization options.
    """
    def __init__(self, x, y, target_x, target_y, speed=7, damage=10, 
                 size=(8, 8), color=BLUE, screen_width=None, screen_height=None,
                 piercing=False, static=False, lifetime=None, homing=False, 
                 effects=None):
        super().__init__()
        
        # Visual properties
        self.size = size
        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Screen boundaries
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT
        
        # Movement properties
        self.speed = speed
        self.homing = homing
        self.target_x = target_x
        self.target_y = target_y
        
        # Calculate initial direction
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx, self.dy = 0, 0
        
        # Combat properties
        self.damage = damage
        self.piercing = piercing
        self.static = static
        self.effects = effects or []  # List of effect functions to apply on hit
        
        # Lifetime management
        self.lifetime = lifetime  # milliseconds, None for infinite
        self.creation_time = pygame.time.get_ticks()
        
        # Hit tracking for piercing and static projectiles
        self.hit_enemies = set() if piercing else None
        self.jump_enemies = set() if static else None
    
    def update(self, enemies=None, *args, **kwargs):
        """Update projectile position and handle homing."""
        # Handle homing behavior
        if self.homing and enemies:
            closest_enemy = self.find_closest_enemy(enemies)
            if closest_enemy:
                self.update_homing_direction(closest_enemy)
        
        # Move projectile
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Check lifetime
        if self.lifetime is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.creation_time > self.lifetime:
                self.kill()
                return
        
        # Remove if out of screen bounds
        if (self.rect.right < -50 or self.rect.left > self.screen_width + 50 or
            self.rect.bottom < -50 or self.rect.top > self.screen_height + 50):
            self.kill()
    
    def find_closest_enemy(self, enemies):
        """Find the closest enemy for homing behavior."""
        if not enemies:
            return None
        
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery
            )
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        
        return closest_enemy
    
    def update_homing_direction(self, target):
        """Update direction to home in on target."""
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            # Gradually adjust direction (not instant turning)
            target_dx = (dx / distance) * self.speed
            target_dy = (dy / distance) * self.speed
            
            # Smooth turning
            turn_rate = 0.1
            self.dx += (target_dx - self.dx) * turn_rate
            self.dy += (target_dy - self.dy) * turn_rate
            
            # Normalize speed
            current_speed = math.hypot(self.dx, self.dy)
            if current_speed != 0:
                self.dx = (self.dx / current_speed) * self.speed
                self.dy = (self.dy / current_speed) * self.speed
    
    def can_hit_enemy(self, enemy):
        """Check if this projectile can hit the given enemy."""
        if not self.piercing:
            return True
        return enemy not in self.hit_enemies
    
    def mark_enemy_hit(self, enemy):
        """Mark an enemy as hit (for piercing projectiles)."""
        if self.piercing and self.hit_enemies is not None:
            self.hit_enemies.add(enemy)
        if self.static and self.jump_enemies is not None:
            self.jump_enemies.add(enemy)
    
    def apply_effects(self, enemy):
        """Apply any special effects to the hit enemy."""
        for effect in self.effects:
            effect(enemy)


class SpecialProjectile(AbilityProjectile):
    """
    Enhanced projectile for special abilities with visual effects.
    """
    def __init__(self, x, y, target_x, target_y, projectile_type="magic_orb", **kwargs):
        self.projectile_type = projectile_type
        super().__init__(x, y, target_x, target_y, **kwargs)
        self.setup_visual()
    
    def setup_visual(self):
        """Setup visual appearance based on projectile type."""
        if self.projectile_type == "magic_orb":
            # Create a glowing orb effect
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            center = (self.size[0] // 2, self.size[1] // 2)
            pygame.draw.circle(self.image, self.color, center, self.size[0] // 2)
            # Add inner glow
            inner_color = tuple(min(255, c + 50) for c in self.color[:3])
            pygame.draw.circle(self.image, inner_color, center, self.size[0] // 3)
            
        elif self.projectile_type == "whisker_beam":
            # Create a beam-like projectile
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, self.color, self.image.get_rect())
            
        elif self.projectile_type == "fur_ball":
            # Create a furry texture
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            center = (self.size[0] // 2, self.size[1] // 2)
            pygame.draw.circle(self.image, self.color, center, self.size[0] // 2)
            # Add texture dots
            for i in range(3):
                for j in range(3):
                    dot_x = (self.size[0] // 4) + i * (self.size[0] // 4)
                    dot_y = (self.size[1] // 4) + j * (self.size[1] // 4)
                    if dot_x < self.size[0] and dot_y < self.size[1]:
                        darker_color = tuple(max(0, c - 30) for c in self.color[:3])
                        pygame.draw.circle(self.image, darker_color, (dot_x, dot_y), 1)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.centerx, self.rect.centery)  # Maintain position
