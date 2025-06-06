import pygame
from abilities.base_ability import PassiveAbility
from utils.settings import *

class FlamingPaws(PassiveAbility):
    """Patas Flamejantes - Adiciona efeito de fogo aos ataques"""
    def __init__(self):
        # Define burn effect function
        def burn_effect(enemy):
            """Apply burn effect to enemy"""
            if not hasattr(enemy, 'is_burning'):
                enemy.is_burning = True
                enemy.burn_start_time = pygame.time.get_ticks()
                enemy.burn_duration = self.burn_duration
                enemy.burn_damage = self.burn_damage
                enemy.last_burn_tick = pygame.time.get_ticks()
                
                # Add visual burn effect
                if not hasattr(enemy, 'burn_particles'):
                    enemy.burn_particles = []
                    
                # Add fire particles around enemy
                for _ in range(8):
                    import random
                    particle = {
                        'x': enemy.rect.centerx + random.randint(-20, 20),
                        'y': enemy.rect.centery + random.randint(-20, 20),
                        'dx': random.uniform(-0.5, 0.5),
                        'dy': random.uniform(-2, -0.5),  # Fire goes up
                        'life': 40,
                        'max_life': 40,
                        'color': (255, random.randint(100, 200), 0)
                    }
                    enemy.burn_particles.append(particle)
        
        # Define projectile modifications for fire effect
        projectile_mods = {
            'color': (255, 69, 0),  # Red-orange for fire
            'visual_effect': 'empowered',
            'particles': 'fire_trail',
            'size': (6, 6),
            'on_hit_effects': [burn_effect],
            'damage_bonus': 1
        }
        
        super().__init__(
            name="Patas Flamejantes",
            description="Ataques causam queimadura nos inimigos e projéteis ficam vermelhos com trilha de fogo",
            stat_name="projectile_damage",
            stat_increase=2,
            projectile_modifications=projectile_mods
        )
        self.burn_duration = 3000  # 3 seconds
        self.burn_damage = 20  # Damage per tick
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add burn effect to player
        player.has_flaming_paws = True
        player.burn_duration = self.burn_duration
        player.burn_damage = self.burn_damage
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.burn_damage += 1
        self.burn_duration += 500
