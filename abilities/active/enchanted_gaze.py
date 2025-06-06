import pygame
import math
import random
from abilities.base_ability import ActiveAbility
from utils.settings import GREEN

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
