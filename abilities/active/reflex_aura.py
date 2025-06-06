import pygame
from abilities.base_ability import BuffAbility

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
