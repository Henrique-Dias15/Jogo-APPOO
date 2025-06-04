import pygame
import math
import random
from abilities.base_ability import *
from entities.ability_projectile import SpecialProjectile, AbilityProjectile
from utils.settings import *

class MysticalMeow(AreaEffectAbility):
    """Miau Místico - Atordoa inimigos próximos e reduz sua defesa mágica"""
    def __init__(self):
        super().__init__(
            name="Miau Místico",
            description="Atordoa inimigos próximos temporariamente",
            cooldown=4000,
            radius=120,
            damage=10
        )
        self.stun_duration = 1500  # 1.5 seconds
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate() or not enemies:
            return False
        
        # Get enemies in range
        enemies_in_range = self.get_enemies_in_range(
            player.rect.centerx, player.rect.centery, enemies
        )
        
        # Apply stun effect
        current_time = pygame.time.get_ticks()
        for enemy in enemies_in_range:
            enemy.take_damage(self.damage)
            # Add stun effect
            enemy.stunned = True
            enemy.stun_end_time = current_time + self.stun_duration
            enemy.original_speed = getattr(enemy, 'original_speed', enemy.speed)
            enemy.speed = 0
        
        self.start_cooldown()
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.stun_duration += 300

class EnchantedGaze(ActiveAbility):
    """Olhar Encantado - Encanta inimigos aleatórios próximos, fazendo-os lutar ao seu lado"""
    def __init__(self):
        super().__init__(
            name="Olhar Encantado",
            description="Converte inimigos próximos em aliados temporários",
            cooldown=8000
        )
        self.charm_radius = 100
        self.charm_duration = 5000  # 5 seconds
        self.max_charmed = 2
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate() or not enemies:
            return False
        
        # Find enemies in range
        enemies_in_range = []
        for enemy in enemies:
            distance = math.hypot(
                enemy.rect.centerx - player.rect.centerx,
                enemy.rect.centery - player.rect.centery
            )
            if distance <= self.charm_radius:
                enemies_in_range.append(enemy)
        
        if not enemies_in_range:
            return False
        
        # Charm random enemies
        charmed_count = min(self.max_charmed, len(enemies_in_range))
        charmed_enemies = random.sample(enemies_in_range, charmed_count)
        
        current_time = pygame.time.get_ticks()
        for enemy in charmed_enemies:
            enemy.charmed = True
            enemy.charm_end_time = current_time + self.charm_duration
            enemy.original_color = enemy.image.get_at((0, 0))  # Store original color
            # Change color to indicate charm
            enemy.image.fill(GREEN)
        
        self.start_cooldown()
        return True
    
    def on_upgrade(self):
        self.max_charmed += 1
        self.charm_duration += 1000

class ReflexAura(BuffAbility):
    """Aura de Reflexos - Aumenta a velocidade de ataque"""
    def __init__(self):
        super().__init__(
            name="Aura de Reflexos",
            description="Aumenta drasticamente a velocidade de ataque",
            cooldown=10000,
            duration=8000,
            buff_effects={'projectile_cooldown': 0.4}  # 60% faster attacks
        )
    
    def activate(self, player, **kwargs):
        if not self.can_activate():
            return False
        
        # Store original cooldown
        self.original_stats['projectile_cooldown'] = player.projectile_cooldown
        # Apply buff
        player.projectile_cooldown = int(player.projectile_cooldown * 0.4)
        
        self.is_active = True
        self.activation_time = pygame.time.get_ticks()
        self.start_cooldown()
        return True

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

class GhostRatSummoning(ActiveAbility):
    """Invocação de Ratos Fantasmas - Invoca ratos mágicos que perseguem e atacam inimigos"""
    def __init__(self):
        super().__init__(
            name="Invocação de Ratos Fantasmas",
            description="Invoca ratos espectrais que caçam inimigos",
            cooldown=7000
        )
        self.rat_count = 3
        self.rat_lifetime = 8000  # 8 seconds
        self.rat_damage = 15
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate():
            return False
        
        projectile_manager = kwargs.get('projectile_manager')
        if not projectile_manager:
            return False
        
        # Create ghost rats that home in on enemies
        for i in range(self.rat_count):
            # Spawn rats in a circle around player
            angle = (360 / self.rat_count) * i
            rad = math.radians(angle)
            
            start_x = player.rect.centerx + math.cos(rad) * 40
            start_y = player.rect.centery + math.sin(rad) * 40
            
            # Target closest enemy or random direction
            target_x, target_y = player.rect.centerx, player.rect.centery
            if enemies:
                closest_enemy = min(enemies, key=lambda e: math.hypot(
                    e.rect.centerx - start_x, e.rect.centery - start_y
                ))
                target_x, target_y = closest_enemy.rect.centerx, closest_enemy.rect.centery
            
            ghost_rat = AbilityProjectile(
                start_x, start_y, target_x, target_y,
                speed=3, damage=self.rat_damage,
                size=(8, 8), color=GREY,
                homing=True, lifetime=self.rat_lifetime
            )
            
            projectile_manager.projectiles.add(ghost_rat)
            projectile_manager.all_sprites.add(ghost_rat)
        
        self.start_cooldown()
        return True
    
    def on_upgrade(self):
        self.rat_count += 1
        self.rat_damage += 5
