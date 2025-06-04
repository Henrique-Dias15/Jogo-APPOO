import pygame
from abilities.base_ability import PassiveAbility

class FrozenClaw(PassiveAbility):
    """Garra Gélida - Adiciona efeitos de congelamento aos ataques"""
    def __init__(self):
        super().__init__(
            name="Garra Gélida",
            description="Ataques têm chance de congelar inimigos",
            stat_name="projectile_damage",
            stat_increase=3
        )
        self.freeze_chance = 0.15  # 15% chance
        self.freeze_duration = 2000  # 2 seconds
    
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add freeze effect to player
        player.has_frozen_claw = True
        player.freeze_chance = self.freeze_chance
        player.freeze_duration = self.freeze_duration
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.freeze_chance += 0.05
