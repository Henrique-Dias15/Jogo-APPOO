import pygame
from utils.settings import *

class HUD:
    """Manages the heads-up display for game information."""
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, clock):
        """Render all HUD elements."""
        self._draw_health_bar()
        self._draw_level_and_exp()
        self._draw_time(clock)
    
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
    
    def _draw_time(self, clock):
        """Display the current game time in minutes:seconds format."""
        # Convert to minutes and seconds
        minutes = int(clock) // 60
        seconds = int(clock) % 60
        
        time_text = self.font.render(
            f"Time: {minutes:02d}:{seconds:02d}", 
            True, WHITE
        )
        
        self.screen.blit(time_text, (10, 100))