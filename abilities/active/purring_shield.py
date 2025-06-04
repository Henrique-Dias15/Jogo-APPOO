import pygame
from abilities.base_ability import BuffAbility

class PurringShield(BuffAbility):
    """Escudo de Ronronar - Cria uma barreira mágica que da dano a inimigos que encostem"""
    def __init__(self):
        super().__init__(
            name="Escudo de Ronronar",
            description="Cria uma barreira que reflete dano aos inimigos",
            cooldown=8000,
            duration=5000,
            buff_effects={}  # No stat changes, just visual effect
        )
        self.shield_damage = 15
        self.shield_radius = 50
    
    def activate(self, player, **kwargs):
        if not self.can_activate():
            return False
        
        # Add shield attribute to player
        player.has_purring_shield = True
        player.shield_damage = self.shield_damage
        player.shield_radius = self.shield_radius
        
        self.is_active = True
        self.activation_time = pygame.time.get_ticks()
        self.start_cooldown()
        return True
    
    def deactivate(self, player, **kwargs):
        super().deactivate(player, **kwargs)
        # Remove shield
        if hasattr(player, 'has_purring_shield'):
            player.has_purring_shield = False
    
    def on_upgrade(self):
        self.shield_damage += 5
        self.shield_radius += 10
