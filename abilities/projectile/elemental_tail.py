import pygame
from abilities.base_ability import ProjectileAbility
from entities.ability_projectile import SpecialProjectile
from utils.settings import ORANGE, RED, CYAN, YELLOW

class ElementalTail(ProjectileAbility):
    """Cauda Elemental - Ataque mágico em linha reta com efeito elemental na direção oposta"""
    def __init__(self):
        super().__init__(
            name="Cauda Elemental",
            description="Dispara energia elemental na direção oposta ao movimento",
            cooldown=2000,
            projectile_class=SpecialProjectile,
            damage=30,
            speed=10,
            size=(8, 20),
            color=ORANGE
        )
        self.elements = ['fire', 'ice', 'lightning']
        self.current_element = 0
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate():
            return False
        
        # Get player's last movement direction (simplified - opposite of center)
        keys = kwargs.get('keys', [])
        direction_x, direction_y = 0, 1  # Default downward
        
        # Determine opposite direction based on movement
        if keys:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                direction_x = 1  # Shoot right if moving left
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction_x = -1  # Shoot left if moving right
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                direction_y = 1  # Shoot down if moving up
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                direction_y = -1  # Shoot up if moving down
        
        # Calculate target position
        target_x = player.rect.centerx + direction_x * 200
        target_y = player.rect.centery + direction_y * 200
        
        # Create elemental projectile
        element = self.elements[self.current_element]
        element_colors = {'fire': RED, 'ice': CYAN, 'lightning': YELLOW}
        
        projectile = SpecialProjectile(
            player.rect.centerx, player.rect.centery,
            target_x, target_y,
            projectile_type="whisker_beam",
            speed=self.speed, damage=self.damage,
            size=self.size, color=element_colors[element],
            piercing=True, lifetime=1500
        )
        
        # Add elemental effect
        if element == 'fire':
            projectile.effects = [self.burn_effect]
        elif element == 'ice':
            projectile.effects = [self.freeze_effect]
        elif element == 'lightning':
            projectile.effects = [self.shock_effect]
        
        # Add to projectile manager
        projectile_manager = kwargs.get('projectile_manager')
        if projectile_manager:
            projectile_manager.projectiles.add(projectile)
            projectile_manager.all_sprites.add(projectile)
        
        # Cycle through elements
        self.current_element = (self.current_element + 1) % len(self.elements)
        self.start_cooldown()
        return True
    
    def burn_effect(self, enemy):
        """Apply burn damage over time"""
        enemy.burning = True
        enemy.burn_end_time = pygame.time.get_ticks() + 3000
        enemy.burn_damage = 5
    
    def freeze_effect(self, enemy):
        """Apply freeze effect"""
        enemy.frozen = True
        enemy.freeze_end_time = pygame.time.get_ticks() + 2000
        enemy.original_speed = getattr(enemy, 'original_speed', enemy.speed)
        enemy.speed = 0
    
    def shock_effect(self, enemy):
        """Apply shock effect that spreads to nearby enemies"""
        enemy.shocked = True
        enemy.shock_end_time = pygame.time.get_ticks() + 1000
