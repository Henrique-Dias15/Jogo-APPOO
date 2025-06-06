import pygame
import math
from abilities.base_ability import ActiveAbility

class FelineTeleport(ActiveAbility):
    """Teleporte Felino - Move-se instantaneamente para uma curta distância à frente"""
    def __init__(self):
        super().__init__(
            name="Teleporte Felino",
            description="Teleporta para uma posição segura",
            cooldown=3000,
            auto_trigger=False  # Manual activation when needed
        )
        self.teleport_distance = 100
    
    def activate(self, player, enemies=None, **kwargs):
        if not self.can_activate():
            return False
        
        # Calculate safe teleport position away from enemies
        best_position = self.find_safe_position(player, enemies)
        if best_position:
            player.rect.centerx, player.rect.centery = best_position
            self.start_cooldown()
            return True
        return False
    
    def find_safe_position(self, player, enemies):
        """Find a safe position to teleport to"""
        if not enemies:
            # No enemies, teleport forward
            return (
                min(max(player.rect.centerx, 50), player.screen_width - 50),
                min(max(player.rect.centery - self.teleport_distance, 50), player.screen_height - 50)
            )
        
        # Try multiple directions to find safe spot
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(angle)
            new_x = player.rect.centerx + math.cos(rad) * self.teleport_distance
            new_y = player.rect.centery + math.sin(rad) * self.teleport_distance
            
            # Keep within screen bounds
            new_x = min(max(new_x, 50), player.screen_width - 50)
            new_y = min(max(new_y, 50), player.screen_height - 50)
            
            # Check if position is safe (far from enemies)
            safe = True
            for enemy in enemies:
                distance = math.hypot(enemy.rect.centerx - new_x, enemy.rect.centery - new_y)
                if distance < 80:  # Too close to enemy
                    safe = False
                    break
            
            if safe:
                return (new_x, new_y)
        
        return None
    
    def on_upgrade(self):
        self.teleport_distance += 20
        self.cooldown = max(self.cooldown - 200, 1000)
