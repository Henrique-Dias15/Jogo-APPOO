from entities.enemys.base_boss import BaseBoss


class BigSquare(BaseBoss):
    """A large boss enemy with high health and damage, moves slowly towards the player."""
    
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, speed=1, hp=500, shooter=False, damage=50):
        # Call the parent constructor with custom parameters
        super().__init__(
            player=player,
            size=(150, 150),  # Larger size for boss
            color=(255, 0, 0),  # Red color for boss
            speed=speed,
            hp=hp,
            shooter=shooter,
            damage=damage,
            x=x,
            y=y,
            screen_width=screen_width,
            screen_height=screen_height,
            spritesheet='assets/images/rumba_boss/Rumba.png',  # Path to the boss sprite sheet
            frame_ammount=3,  # Single frame for simplicity, can be animated later
            turn=True
        )
    
    def kill(self):
        """Handle boss death, drop experience, and remove from groups"""
        return super().kill(50)  # Drop more experience on death