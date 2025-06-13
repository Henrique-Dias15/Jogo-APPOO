from utils.settings import *
from entities.enemys.base_enemy import BaseEnemy
class Enemy(BaseEnemy):
    """Base enemy class that can be extended for different enemy types"""
    def __init__(self, player, x=None, y=None, screen_width=None, screen_height=None, 
                 size=(20, 20), color=RED, speed=ENEMY_SPEED, hp=ENEMY_HP, shooter=False, damage=ENEMY_DAMAGE):
        super().__init__(player = player, size=size, color=color, speed=speed, hp=hp, shooter=shooter, damage=damage, x=x, y=y, screen_width=screen_width, screen_height=screen_height)