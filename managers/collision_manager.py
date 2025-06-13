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
            # Initialize piercing hit tracking
            if getattr(projectile, 'piercing', False) and not hasattr(projectile, 'hit_enemies'):
                projectile.hit_enemies = set()
            
            hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False)
            
            for enemy in hit_enemies:
                # Skip if already hit by piercing projectile
                if getattr(projectile, 'piercing', False) and enemy in projectile.hit_enemies:
                    continue

                # Apply damage once per enemy
                if enemy.take_damage(projectile.damage):
                    self.player.gain_exp(10)
                    enemy.kill()
                    killed_enemies.append(enemy)

                # Apply special effects
                self.apply_projectile_effects(projectile, enemy)

                # Handle piercing logic
                if getattr(projectile, 'piercing', False):
                    # Initialize hit tracking if missing
                    if not hasattr(projectile, 'hit_enemies') or projectile.hit_enemies is None:
                        projectile.hit_enemies = set()
                    # Track hit enemy
                    projectile.hit_enemies.add(enemy)
                    # Check max pierces
                    max_pierces = getattr(projectile, 'max_pierces', None)
                    if max_pierces is not None and len(projectile.hit_enemies) >= max_pierces:
                        projectile.kill()
                        break
                    # Continue piercing
                    continue

                # Non-piercing projectile: remove after hit
                projectile.kill()
                break
         
        return killed_enemies

    def check_projectile_player_collisions(self, projectiles):
        """Check for collisions between projectiles and player"""
        collided_projectiles = []
        for projectile in projectiles:
            if pygame.sprite.collide_rect(projectile, self.player):
                # Handle player hit by projectile
                self.player.hp -= projectile.damage
                projectile.kill()
                collided_projectiles.append(projectile)

        return collided_projectiles, self.player.hp <= 0
                    
    def check_enemy_player_collisions(self, enemies):
        """Check for collisions between enemies and player"""
        collided_enemies = []
        
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, self.player):
              # Normal collision damage
                damage = enemy.damage if hasattr(enemy, 'damage') else 10
                self.player.hp -= damage
                enemy.kill()
                collided_enemies.append(enemy)
                
        return collided_enemies, self.player.hp <= 0
    
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
                
        # Apply cleaning tongue effect
        if (hasattr(self.player, 'has_cleaning_tongue') and self.player.has_cleaning_tongue and 
            random.random() < self.player.heal_chance):
            heal_amount = int(self.player.max_hp * self.player.heal_amount)
            self.player.hp = min(self.player.max_hp, self.player.hp + heal_amount)
            
        # Apply pawquake effect
        if (hasattr(self.player, 'has_pawquake') and self.player.has_pawquake):
            # Knock back enemy
            knockback_vector = pygame.math.Vector2(enemy.rect.center) - pygame.math.Vector2(self.player.rect.center)
            knockback_vector.scale_to_length(self.player.knockback_distance)
            enemy.rect.move_ip(knockback_vector.x, knockback_vector.y)
            
        # Apply steel whiskers effect
        if hasattr(self.player, 'has_steel_whiskers') and self.player.has_steel_whiskers:
            # Enable piercing on projectile and set max pierces
            projectile.piercing = True
            projectile.max_pierces = getattr(self.player, 'piercing_count', None)
            # If projectile has a piercing effect, apply it
            if hasattr(projectile, 'pierce_effect'):
                projectile.pierce_effect(enemy)
         
        # Apply projectile-specific effects
        if hasattr(projectile, 'apply_effects'):
            projectile.apply_effects(enemy)