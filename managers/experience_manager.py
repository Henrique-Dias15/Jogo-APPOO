import pygame
from entities.enemys.base_enemy import BaseEnemy
from entities.player.player import Player
class ExperienceManager:
    def __init__(self, player:Player) -> None:
        self.player = player
        self.experience_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def kill_enemy(self, enemy:BaseEnemy) -> None:
        """Handle enemy death, drop experience, and remove from groups"""
        xp = enemy.kill()
        self.experience_group.add(xp)
        self.all_sprites.add(xp)
        return None
    
    def draw(self, screen:pygame.Surface) -> None:
        """Draw all experience sprites on the screen"""
        self.experience_group.draw(screen)

    def reset(self) -> None:
        """Clear all enemies"""
        self.experience_group.empty()
        self.all_sprites.empty()