import pygame

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
                if enemy.take_damage(projectile.damage):
                    # Enemy destroyed, give player experience
                    self.player.gain_exp(10)
                    enemy.kill()
                    killed_enemies.append(enemy)
                projectile.kill()
                
        return killed_enemies
    
    def check_enemy_player_collisions(self, enemies):
        """Check for collisions between enemies and player"""
        collided_enemies = []
        
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, self.player):
                self.player.hp -= enemy.damage if hasattr(enemy, 'damage') else 10
                enemy.kill()
                collided_enemies.append(enemy)
                
        return collided_enemies, self.player.hp <= 0