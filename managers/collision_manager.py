import pygame
import random

class CollisionManager:
    """
    Handles all collision detection and resolution in the game.
    """
    def __init__(self, player):
        self.player = player
    
    def check_projectile_enemy_collisions(self, projectiles, enemies):
        """Check for collisions between projectiles and enemies"""
        killed_enemies = []
        
        for projectile in projectiles:
            hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False)
            
            for enemy in hit_enemies:
                # Check if projectile can hit this enemy (for piercing projectiles)
                if hasattr(projectile, 'can_hit_enemy') and not projectile.can_hit_enemy(enemy):
                    continue
                
                # Apply damage
                if enemy.take_damage(projectile.damage):
                    # Enemy destroyed, give player experience
                    self.player.gain_exp(10)
                    enemy.kill()
                    killed_enemies.append(enemy)
                
                # Apply special effects
                self.apply_projectile_effects(projectile, enemy)
                
                # Handle explosion damage
                if hasattr(projectile, 'explosion_radius') and projectile.explosion_radius > 0:
                    explosion_enemies = projectile.explode(enemies)
                    for exp_enemy in explosion_enemies:
                        if exp_enemy != enemy:  # Don't double damage the direct hit
                            if exp_enemy.take_damage(projectile.damage // 2):  # Half damage for explosion
                                self.player.gain_exp(10)
                                exp_enemy.kill()
                                killed_enemies.append(exp_enemy)
                
                # Mark enemy as hit for piercing projectiles
                if hasattr(projectile, 'mark_enemy_hit'):
                    projectile.mark_enemy_hit(enemy)
                
                # Remove projectile if it's not piercing
                if not hasattr(projectile, 'piercing') or not projectile.piercing:
                    projectile.kill()
                    break
                
        return killed_enemies
    
    def check_enemy_player_collisions(self, enemies):
        """Check for collisions between enemies and player"""
        collided_enemies = []
        
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, self.player):
                # Check if player has purring shield
                if hasattr(self.player, 'has_purring_shield') and self.player.has_purring_shield:
                    # Shield reflects damage back to enemy
                    if enemy.take_damage(self.player.shield_damage):
                        self.player.gain_exp(10)
                        enemy.kill()
                        collided_enemies.append(enemy)
                        continue
                
                # Normal collision damage
                damage = enemy.damage if hasattr(enemy, 'damage') else 10
                self.player.hp -= damage
                enemy.kill()
                collided_enemies.append(enemy)
        
        # Check shield area damage
        if hasattr(self.player, 'has_purring_shield') and self.player.has_purring_shield:
            self.check_shield_area_damage(enemies, collided_enemies)
                
        return collided_enemies, self.player.hp <= 0
    
    def check_shield_area_damage(self, enemies, collided_enemies):
        """Check for enemies within shield radius and damage them"""
        import math
        
        for enemy in enemies:
            if enemy in collided_enemies:
                continue
                
            distance = math.hypot(
                enemy.rect.centerx - self.player.rect.centerx,
                enemy.rect.centery - self.player.rect.centery
            )
            
            if distance <= self.player.shield_radius:
                if enemy.take_damage(self.player.shield_damage // 3):  # Reduced shield aura damage
                    self.player.gain_exp(5)
                    enemy.kill()
                    collided_enemies.append(enemy)
    
    def apply_projectile_effects(self, projectile, enemy):
        """Apply special effects from projectiles to enemies"""
        # Apply frozen claw effect
        if (hasattr(self.player, 'has_frozen_claw') and self.player.has_frozen_claw and 
            random.random() < self.player.freeze_chance):
            enemy.frozen = True
            enemy.freeze_end_time = pygame.time.get_ticks() + self.player.freeze_duration
            enemy.original_speed = getattr(enemy, 'original_speed', enemy.speed)
            enemy.speed = 0
        
        # Apply flaming paws effect
        if (hasattr(self.player, 'has_flaming_paws') and self.player.has_flaming_paws):
            enemy.burning = True
            enemy.burn_end_time = pygame.time.get_ticks() + self.player.burn_duration
            enemy.burn_damage = self.player.burn_damage
            # Don't change speed for burning enemies - they can still move while burning
                
            # Start burn damage timer
            if not hasattr(enemy, 'last_burn_tick'):
                enemy.last_burn_tick = pygame.time.get_ticks()
        
        # Apply projectile-specific effects
        if hasattr(projectile, 'apply_effects'):
            projectile.apply_effects(enemy)