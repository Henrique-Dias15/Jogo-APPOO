import pygame
from utils.settings import *

class GameStateManager:
    """
    Manages game states and transitions.
    """
    def __init__(self):
        # Game states
        self.MAIN_MENU = "main_menu"
        self.PLAYING = "playing"
        self.LEVEL_UP = "level_up"
        self.GAME_OVER = "game_over"
        self.GAME_WON = "game_won"
        
        # Current state
        self.current_state = self.MAIN_MENU
        
        # Level up options
        self.upgrade_options = []
    
    def change_state(self, new_state):
        """Change to a new game state"""
        self.current_state = new_state
    
    def is_state(self, state):
        """Check if current state matches the given state"""
        return self.current_state == state
    
    def set_level_up_options(self, options):
        """Set available upgrade options for level up screen"""
        self.upgrade_options = options
        
    def handle_game_over_input(self, event):
        """Handle input during game over state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                self.current_state = self.PLAYING  # Changed from MAIN_MENU to PLAYING
                return True
            elif event.key == pygame.K_q:
                # Quit the game
                return False
        return True
    
    def handle_game_won_input(self, event):
        """Handle input during game won state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                self.current_state = self.PLAYING  # Changed from MAIN_MENU to PLAYING
                return True
            elif event.key == pygame.K_q:
                # Quit the game
                return False  # This needs to return False to signal quitting
        return True
    
    def handle_level_up_input(self, event, menu_system, player_level, option_rects, ability_manager):
        """Handle input during level up state"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    # Apply the selected upgrade
                    if i < len(self.upgrade_options):
                        ability_name = self.upgrade_options[i]['ability']
                        ability_manager.upgrade_ability(ability_name)
                        
                        # Resume game
                        self.current_state = self.PLAYING
                        return True
            
        return True