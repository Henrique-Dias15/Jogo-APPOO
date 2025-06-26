import pygame
from utils.settings import *
from typing import Optional
from ui.menu import MenuSystem
from managers.ability_manager import AbilityManager

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
        self.INPUTTING_NAME = "inputting_name"
        
        # Current state
        self.current_state = self.MAIN_MENU
        
        # Level up options
        self.upgrade_options = []
    
    def change_state(self, new_state:str)->None:
        """Change to a new game state"""
        self.current_state = new_state
    
    def is_state(self, state:str)->bool:
        """Check if current state matches the given state"""
        return self.current_state == state
    
    def set_level_up_options(self, options:list[dict])->None:
        """Set available upgrade options for level up screen"""
        self.upgrade_options = options

    def handle_name_input(self, event, current_name:Optional[str]="", max_length:Optional[int]=10) -> tuple[str, bool]:
        """Handle input for name entry"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Confirm name input
                if current_name:
                    self.current_state = self.PLAYING
                    return current_name, True
                return current_name, False
            elif event.key == pygame.K_BACKSPACE:
                # Remove last character
                current_name = current_name[:-1]
                return current_name, False
            else:
                # Add new character if within limits and printable
                if len(current_name) < max_length and event.unicode.isprintable():
                    current_name += event.unicode
                return current_name, False
        
        return current_name, False
        
    def handle_game_over_input(self, event: pygame.event.Event) -> bool:
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
    
    def handle_game_won_input(self, event: pygame.event.Event) -> bool:
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
    
    def handle_level_up_input(self, event, menu_system:MenuSystem, player_level:int, option_rects:list[dict], ability_manager:AbilityManager) -> bool:
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