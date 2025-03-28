import pygame
from utils.settings import *

class MenuSystem:
    """Manages different game menus and state transitions."""
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 64)
        self.font_menu = pygame.font.Font(None, 48)
    
    def draw_start_menu(self):
        """Render the game's start menu."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_title.render(
            "Magical Cat Game", 
            True, WHITE
        )
        title_rect = title.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        )
        
        # Subtitle
        subtitle = self.font_menu.render(
            "Press ENTER to Start", 
            True, GREEN
        )
        subtitle_rect = subtitle.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        )
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
    
    def draw_game_over(self, player_level):
        """Render the game over screen."""
        self.screen.fill(BLACK)
        
        # Game Over Text
        game_over = self.font_title.render(
            "Game Over", 
            True, RED
        )
        game_over_rect = game_over.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        )
        
        # Level Reached
        level_text = self.font_menu.render(
            f"You reached Level {player_level}", 
            True, WHITE
        )
        level_rect = level_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        )
        
        # Restart Instructions
        restart_text = self.font_menu.render(
            "Press R to Restart", 
            True, GREEN
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
        )
        
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(restart_text, restart_rect)