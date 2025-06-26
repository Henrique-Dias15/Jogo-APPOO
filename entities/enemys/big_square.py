from entities.enemys.base_boss import BaseBoss
import pygame
from entities.player.player import Player
from typing import Optional
from entities.experience.experience import Experience
class BigSquare(BaseBoss):
    """A large boss enemy with high health and damage, moves slowly towards the player."""
    
    def __init__(self, 
        player: Player, 
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        screen_width: Optional[float] = None, 
        screen_height: Optional[float] = None, 
        speed: Optional[float] = 1, 
        hp: Optional[int] = 500, 
        shooter: Optional[bool] = False, 
        damage: Optional[float] = 50
    ) -> None:
        # Call the parent constructor with custom parameters
        size = (150, 150)  # Larger size for boss
        color = (255, 0, 0)  # Red color for boss
        super().__init__(
            player=player,
            size=size,  # Larger size for boss
            color=color,  # Red color for boss
            speed=speed,
            hp=hp,
            shooter=shooter,
            damage=damage,
            x=x,
            y=y,
            screen_width=screen_width,
            screen_height=screen_height,
            spritesheet="assets/images/enemys/rumba_boss/Rumba.png",  # Path to the boss spritesheet,
            frame_ammount=3,
            frame_delay=100
        )
        
    
    def kill(self) -> Experience:
        """Handle boss death, drop experience, and remove from groups"""
        return super().kill(50)  # Drop more experience on death
    
    def update(self, *args, **kwargs) -> None:
        result = super().update()
        if result == 0:
            return
        self.update_animation_rotation()