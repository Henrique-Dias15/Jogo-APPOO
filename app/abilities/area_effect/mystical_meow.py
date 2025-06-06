import pygame
from abilities.base_ability import AreaEffectAbility

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
