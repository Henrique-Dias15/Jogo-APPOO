import pygame
from entities.player.player import Player
from typing import Optional
class Experience(pygame.sprite.Sprite):
    """Class representing experience points in the game."""
    
    def __init__(self, player: Player, x: float, y: float, value: Optional[int] = 10) -> None:
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 215, 0))  # Gold color for experience
        self.rect = self.image.get_rect(center=(x, y))
        self.value = value
        self.player = player
        

    def kill(self) -> None:
        """Override kill to add experience to player"""
        self.player.gain_exp(self.value)
        super().kill()
