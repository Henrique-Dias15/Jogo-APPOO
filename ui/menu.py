import pygame
from utils.settings import *
from utils.database import DatabaseManager
import time as tm
class MenuSystem:
    """Manages different game menus and state transitions."""
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 64)
        self.font_menu = pygame.font.Font(None, 48)
        
        # Get the actual screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def draw_start_menu(self):
        """Render the game's start menu."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_title.render(
            GAME_TITLE, 
            True, WHITE
        )
        title_rect = title.get_rect(
            center=(self.width//2, self.height//2 - 100)
        )
        
        # Subtitle
        subtitle = self.font_menu.render(
            "Press ENTER to Start", 
            True, GREEN
        )
        subtitle_rect = subtitle.get_rect(
            center=(self.width//2, self.height//2)
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
            center=(self.width//2, self.height//2 - 100)
        )
        
        # Level Reached
        level_text = self.font_menu.render(
            f"You reached Level {player_level}", 
            True, WHITE
        )
        level_rect = level_text.get_rect(
            center=(self.width//2, self.height//2)
        )
        
        ranking_text = self.font_menu.render(
            "Top 10 Rankings:",
            True, WHITE
        )
        ranking_rect = ranking_text.get_rect(
            center=(self.width//2, self.height//9 + self.height//9)
        )

        self.screen.blit(ranking_text, ranking_rect)
        # # Fetch and display rankings
        rankings = self.databaseManager.listar_rankings()
        y_offset = 0
        for i, (name, time) in enumerate(rankings):
            rank_text = self.font_menu.render(
                f"{i + 1}. {name} - {tm.strftime(
                    "%M:%S" if time < 3600 else "%H:%M:%S", tm.gmtime(time)
                )}", 
                True, WHITE
            )
            rank_rect = rank_text.get_rect(
                center=(self.width//2, self.height//9 + self.height//6 + y_offset)
            )
            self.screen.blit(rank_text, rank_rect)
            y_offset += self.height // 18
            

        # Restart Instructions
        restart_text = self.font_menu.render(
            "Press R to Restart", 
            True, GREEN
        )
        restart_rect = restart_text.get_rect(
            center=(self.width//2, self.height//2 + 100)
        )
        
        # Quit game instructions
        quit_text = self.font_menu.render(
            "Press Q to Quit", 
            True, GREEN
        )
        quit_rect = quit_text.get_rect(
            center=(self.width//2, self.height//2 + 150)
        )
        
        self.screen.blit(quit_text, quit_rect)
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(restart_text, restart_rect)
        
    def draw_level_up(self, player_level, upgrade_options):
        """Render the level up screen with upgrade options."""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Level Up Title
        level_up_text = self.font_title.render(
            f"Level Up! Level {player_level}", 
            True, GREEN
        )
        level_up_rect = level_up_text.get_rect(
            center=(self.width//2, self.height//2 - 150)
        )
        self.screen.blit(level_up_text, level_up_rect)
        
        # Choose Upgrade Text
        choose_text = self.font_menu.render(
            "Choose an Upgrade:", 
            True, WHITE
        )
        choose_rect = choose_text.get_rect(
            center=(self.width//2, self.height//2 - 80)
        )
        self.screen.blit(choose_text, choose_rect)
        
        # Draw Upgrade Options
        option_rects = []
        y_offset = -20
        for i, option in enumerate(upgrade_options):
            # Create option button
            option_rect = pygame.Rect(self.width//2 - 150, self.height//2 + y_offset, 300, 60)
            pygame.draw.rect(self.screen, BLUE, option_rect, 0, 10)
            pygame.draw.rect(self.screen, WHITE, option_rect, 2, 10)
            
            # Option text
            option_text = self.font_menu.render(
                option['name'], 
                True, WHITE
            )
            option_text_rect = option_text.get_rect(
                center=option_rect.center
            )
            self.screen.blit(option_text, option_text_rect)
            
            option_rects.append(option_rect)
            y_offset += 80
        
        return option_rects  # Return clickable regions
    
    def draw_game_won(self, player_level):
        """Render the game over screen."""
        self.screen.fill(BLACK)
        
        # Game Over Text
        game_over = self.font_title.render(
            "You Win!", 
            True, BLUE
        )
        game_over_rect = game_over.get_rect(
            center=(self.width//2, self.height//2 - 100)
        )
        
        # Level Reached
        level_text = self.font_menu.render(
            f"You reached Level {player_level}", 
            True, WHITE
        )
        level_rect = level_text.get_rect(
            center=(self.width//2, self.height//2)
        )
        
        # Restart Instructions
        restart_text = self.font_menu.render(
            "Press R to Restart", 
            True, GREEN
        )
        restart_rect = restart_text.get_rect(
            center=(self.width//2, self.height//2 + 100)
        )
        
        # Quit game instructions
        quit_text = self.font_menu.render(
            "Press Q to Quit", 
            True, RED
        )
        quit_rect = quit_text.get_rect(
            center=(self.width//2, self.height//2 + 150)
        )
        
        self.screen.blit(quit_text, quit_rect)
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(restart_text, restart_rect)