import pygame
from entities.projectiles.projectile import Projectile
import math
from entities.player.player import Player
from entities.enemys.base_enemy import BaseEnemy
from typing import Optional
class ProjectileManager:
    """
    Handles projectile creation, tracking, and updates.
    """
    def __init__(self, player:Player, screen_width:float, screen_height:float) -> None:
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()

    def create_projectile(self, shooter:Player|BaseEnemy, target_x:float, target_y:float, is_player:Optional[bool] = True, angle:Optional[float] = None) -> Optional[Projectile]:
        """Create a projectile targeting the specified coordinates"""
        if shooter.can_shoot():
            # Check if player has projectile modifications from passive abilities
            modifications = getattr(shooter, 'projectile_modifications', {})
            if modifications:
                # Use enhanced projectile with modifications
                projectile = Projectile(
                    shooter.rect.centerx, 
                    shooter.rect.centery,
                    target_x, 
                    target_y,
                    screen_width=self.screen_width,
                    screen_height=self.screen_height,
                    damage=shooter.projectile_damage,
                    modifications=modifications, 
                    angle=angle,
                    is_player_projectile=is_player,
                )
            else:
                # Use basic projectile
                projectile = Projectile(
                    shooter.rect.centerx, 
                    shooter.rect.centery,
                    target_x, 
                    target_y,
                    screen_width=self.screen_width,
                    screen_height=self.screen_height,
                    damage=shooter.projectile_damage,
                    is_player_projectile=is_player,
                )
            
            if is_player:
                self.player_projectiles.add(projectile)
            else:
                self.enemy_projectiles.add(projectile)

            self.projectiles.add(projectile)
            self.all_sprites.add(projectile)
            
            # Update last shot time
            shooter.last_shot = pygame.time.get_ticks()
            return projectile
            
        return None
            
    def handle_auto_shooting(self, enemies:list[BaseEnemy]) -> Optional[Projectile]:
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
                angle = math.degrees(math.atan2(-dy, dx))  # Calculate angle to enemy
        
        if closest_enemy:
            return self.create_projectile(self.player, closest_enemy.rect.centerx, closest_enemy.rect.centery,is_player=True, angle=angle)

        return None
    
    def handle_enemy_auto_shooting(self, enemies:list[BaseEnemy]) -> Optional[Projectile]:
        """Automatically target player and create projectile for enemies"""
        for enemy in enemies:
            if enemy.shooter and enemy.can_shoot():
                dx = self.player.rect.centerx - enemy.rect.centerx
                dy = self.player.rect.centery - enemy.rect.centery

                angle = math.degrees(math.atan2(-dy, dx))  # Calculate angle to player
                # Use enemy's shooter method to create projectile
                return self.create_projectile(
                    enemy, 
                    self.player.rect.centerx, 
                    self.player.rect.centery, 
                    is_player=False,
                    angle=angle
                )

    def update(self, enemies:list[BaseEnemy]=None, *args, **kwargs)-> None:
        """Update all projectiles, passing enemies for homing projectiles"""
        for projectile in self.projectiles:
            if hasattr(projectile, 'update'):
                if enemies is not None:
                    projectile.update(enemies, *args, **kwargs)
                else:
                    projectile.update(*args, **kwargs)
        
    def draw(self, screen:pygame.Surface) -> None:
        """Draw all projectiles"""
        for projectile in self.projectiles:
            if hasattr(projectile, 'draw') and callable(projectile.draw):
                # Enhanced projectiles have custom draw method with particles
                projectile.draw(screen)
            else:
                # Basic projectiles use standard sprite drawing
                screen.blit(projectile.image, projectile.rect)
    
    def reset(self) -> None:
        """Clear all projectiles"""
        self.projectiles.empty()
        self.all_sprites.empty()