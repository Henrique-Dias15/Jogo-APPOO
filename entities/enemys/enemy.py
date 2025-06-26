from utils.settings import *
from entities.enemys.base_enemy import BaseEnemy
from entities.player.player import Player
from typing import Optional, Tuple
from entities.experience.experience import Experience
class Enemy(BaseEnemy):
    """Base enemy class that can be extended for different enemy types"""
    def __init__(self,
        player: Player, 
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        screen_width: Optional[float] = None, 
        screen_height: Optional[float] = None, 
        size: Optional[Tuple[int, int]] = (100, 100), 
        color: Optional[Tuple[int,int,int]] = RED, 
        speed: Optional[float] = ENEMY_SPEED, 
        hp: Optional[int] = ENEMY_HP, 
        shooter: Optional[bool] = False, 
        damage: Optional[float] = ENEMY_DAMAGE
    ) -> None:
        super().__init__(
            player = player, 
            size=size, 
            color=color,
            speed=speed, 
            hp=hp, 
            shooter=shooter, 
            damage=damage, 
            x=x, 
            y=y, 
            screen_width=screen_width, 
            screen_height=screen_height,
            spritesheet='assets/images/enemys/rat/Rato.png',
            frame_ammount=2,  # Number of frames in the sprite sheet
            frame_delay=150,
        )

    def update(self, *args, **kwargs) -> None:
        """Update the enemy's position and state"""
        result = super().update(*args, **kwargs)
        if result == 0:
            return
        self.update_animation_turning()
        


    def kill(self) -> Experience:
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(10)