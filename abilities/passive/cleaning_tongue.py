from abilities.base_ability import PassiveAbility

class CleaningTongue(PassiveAbility):
    """Cleaning Tongue - Basic shots have a chance to heal a % of max HP on hit"""
    def __init__(self):
        # Define projectile modifications for healing effect
        projectile_mods = {
            'color': (28, 163, 236),  # Water Color
            'visual_effect': 'healing',
            'particles': 'healing_trail',  # Not working for now
            'size': (7, 7),
            'spritesheet': 'assets/images/water/Water.png',
            'sprite_frame_delay': 100,
        }

        super().__init__(
            name="Cleaning Tongue",
            description="Basic shots have a chance to heal a % of max HP on hit",
            stat_name="",
            stat_increase=0,  # No stat increase for this ability
            projectile_modifications=projectile_mods
        )
        self.heal_chance = 0.05
        self.heal_amount = 0.15
        
    def activate(self, player, **kwargs):
        super().activate(player, **kwargs)
        # Add healing effect to player
        player.has_cleaning_tongue = True
        player.heal_chance = self.heal_chance
        player.heal_amount = self.heal_amount
        return True
    
    def on_upgrade(self):
        super().on_upgrade()
        self.heal_chance += 0.05
        self.heal_amount += 0.01