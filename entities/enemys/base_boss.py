from entities.enemys.base_enemy import BaseEnemy
import pygame
from entities.player.player import Player
from typing import Optional, Tuple
class BaseBoss(BaseEnemy):
    """
    Base class for all bosses in the game.
    Inherits from BaseEnemy and can be extended with boss-specific attributes and methods.
    """
    
    def __init__(self, 
        player:Player, 
        size:Tuple, 
        color:Tuple, 
        speed:float, 
        hp:int, 
        shooter:bool, 
        damage:float, 
        x:Optional[float]=None, 
        y:Optional[float]=None, 
        screen_width:Optional[float]=None, 
        screen_height:Optional[float]=None, 
        spritesheet:Optional[str]=None, 
        frame_ammount:Optional[int]=None, 
        frame_delay:Optional[float]=None
    ) -> None:
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        if x is None or y is None:
            temp_rect = pygame.Rect(center_x, center_y, size[0], size[1])
            temp_rect.center = (center_x, center_y)
            if temp_rect.colliderect(player.rect):
                # If the boss spawns on the player, adjust position
                x = None
                y = None
            else:
                x, y = temp_rect.center
        
        super().__init__(player=player, size=size, color=color, speed=speed, hp=hp, shooter=shooter, damage=damage, x=x, y=y, screen_width=screen_width, screen_height=screen_height, spritesheet=spritesheet, frame_ammount=frame_ammount, frame_delay=frame_delay)
        self.is_boss = True  # Flag to indicate this is a boss enemy
        self.max_hp = hp  # Store max HP for health bar calculations

    