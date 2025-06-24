from utils.settings import *
from entities.enemys.base_enemy import BaseEnemy
class Enemy(BaseEnemy):
    """Base enemy class that can be extended for different enemy types"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, 
                 size=(100, 100), color=RED, speed=ENEMY_SPEED, hp=ENEMY_HP, shooter=False, damage=ENEMY_DAMAGE):
        super().__init__(player = player, 
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
            spritesheet='assets/images/rat/Rato.png',
            frame_ammount=2,  # Number of frames in the sprite sheet
        )

    def update(self, *args, **kwargs):
        """Update the enemy's position and state"""
        result = super().update(*args, **kwargs)
        if result == 0:
            return
        self.update_animation_turning()
        


    def kill(self):
        """Handle enemy death, drop experience, and remove from groups"""
        return super().kill(10)