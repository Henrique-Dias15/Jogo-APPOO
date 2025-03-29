import pygame
from entities.projectile import Projectile

class ProjectileManager:
    """
    Handles projectile creation, tracking, and updates.
    """
    def __init__(self, player, screen_width, screen_height):
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
    
    def create_projectile(self, target_x, target_y):
        """Create a projectile targeting the specified coordinates"""
        if self.player.can_shoot():
            projectile = Projectile(
                self.player.rect.centerx, 
                self.player.rect.centery,
                target_x, 
                target_y,
                screen_width=self.screen_width,
                screen_height=self.screen_height,
                damage=self.player.projectile_damage
            )
            
            self.projectiles.add(projectile)
            self.all_sprites.add(projectile)
            
            # Update last shot time
            self.player.last_shot = pygame.time.get_ticks()
            return projectile
            
        return None
            
    def handle_auto_shooting(self, enemies):
        """Automatically target nearest enemy and create projectile"""
        if not self.player.can_shoot() or not enemies:
            return None
            
        # Find the closest enemy to target
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            # Calculate distance between player and this enemy
            dx = enemy.rect.centerx - self.player.rect.centerx
            dy = enemy.rect.centery - self.player.rect.centery
            distance = (dx**2 + dy**2)**0.5  # Euclidean distance
            
            # Update closest enemy if this one is closer
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        
        if closest_enemy:
            return self.create_projectile(closest_enemy.rect.centerx, closest_enemy.rect.centery)
        
        return None
    
    def update(self, *args, **kwargs):
        """Update all projectiles"""
        self.projectiles.update(*args, **kwargs)
        
    def draw(self, screen):
        """Draw all projectiles"""
        self.projectiles.draw(screen)
    
    def reset(self):
        """Clear all projectiles"""
        self.projectiles.empty()
        self.all_sprites.empty()