import pygame
from utils.settings import *

class HUD:
    """Manages the heads-up display for game information."""
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
    
    def draw(self):
        """Render all HUD elements."""
        self._draw_health_bar()
        self._draw_level_and_exp()
    
    def _draw_health_bar(self):
        """Draw player's health bar."""
        bar_width = 200
        bar_height = 20
        fill_width = int((self.player.hp / self.player.max_hp) * bar_width)
        
        # Outline
        pygame.draw.rect(self.screen, WHITE, 
            (10, 10, bar_width, bar_height), 2)
        
        # Fill
        pygame.draw.rect(self.screen, RED, 
            (10, 10, fill_width, bar_height))
    
    def _draw_level_and_exp(self):
        """Display player's level and experience."""
        level_text = self.font.render(
            f"Level: {self.player.level}", 
            True, WHITE
        )
        exp_text = self.font.render(
            f"EXP: {self.player.exp}/100", 
            True, WHITE
        )
        
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(exp_text, (10, 70))