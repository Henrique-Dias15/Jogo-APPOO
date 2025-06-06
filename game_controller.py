import pygame
import sys
from utils.settings import *
from entities.player import Player
from ui.hud import HUD
from ui.menu import MenuSystem
from abilities.ability_manager import AbilityManager
from managers.enemy_spawner import EnemyManager
from managers.projectile_manager import ProjectileManager
from managers.collision_manager import CollisionManager
from managers.game_state_manager import GameStateManager

class GameController:
    """
    Primary game management class responsible for coordinating game systems.
    """
    def __init__(self):
        """Initialize the game with all necessary components."""
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        
        # Screen and timing setup
        if FULLSCREEN:
            info = pygame.display.Info()
            self.width, self.height = info.current_w, info.current_h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
            self.screen = pygame.display.set_mode((self.width, self.height))
        
        # Initialize clock for timing and frame rate control
        self.clock = pygame.time.Clock()
        self.elapsed_time = 0
                
        # UI Systems
        self.menu_system = MenuSystem(self.screen)
        
        # Game state manager
        self.state_manager = GameStateManager()
        
        # Initialize game state
        self.reset_game_state()
    
    def reset_game_state(self):
        """Reset all game variables to their initial state."""
        # All sprites group for rendering
        self.all_sprites = pygame.sprite.Group()
        
        # Create player at screen center
        self.player = Player(self.width // 2, self.height // 2, 
                           screen_width=self.width, screen_height=self.height)
        self.all_sprites.add(self.player)
        
        # Create HUD for the player
        self.hud = HUD(self.player, self.screen)
        
        # Create ability manager
        self.ability_manager = AbilityManager(self.player)
        
        # Create game managers
        self.enemy_manager = EnemyManager(self.player, self.width, self.height)
        self.projectile_manager = ProjectileManager(self.player, self.width, self.height)
        self.collision_manager = CollisionManager(self.player)
        
        # Connect player level up to game controller
        self.player.set_level_up_callback(self.trigger_level_up)
        
        # Don't reset the game state here unless starting from scratch
        # We'll reset elapsed_time when transitioning from menu to playing
    
    def trigger_level_up(self):
        """Pause game and show level up screen."""
        self.state_manager.change_state(self.state_manager.LEVEL_UP)
        self.state_manager.set_level_up_options(self.ability_manager.get_upgrade_options())
    
    def trigger_game_over(self):
        """Set game over state and prepare for restart/exit."""
        self.state_manager.change_state(self.state_manager.GAME_OVER)
        self.clear_game_entities()
        
    def trigger_game_won(self):
        """Set game won state and prepare for restart/exit."""
        self.state_manager.change_state(self.state_manager.GAME_WON)
        self.clear_game_entities()
        
    def clear_game_entities(self):
        """Clear all game entities."""
        self.all_sprites.empty()
        self.enemy_manager.reset()
        self.projectile_manager.reset()
    
    def run(self):
        """Main game loop that manages different game states."""
        # Start with the main menu
        self.show_start_menu()
        
        running = True
        while running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Game over state event handling
                if self.state_manager.is_state(self.state_manager.GAME_OVER):
                    running = self.state_manager.handle_game_over_input(event)
                    if not running:
                        break  # Exit the loop if we should quit
                    
                    # Only reset if we're continuing (R was pressed)
                    if self.state_manager.is_state(self.state_manager.PLAYING):
                        self.reset_game_state()
                        self.elapsed_time = 0  # Reset timer when restarting after game over
                        
                # Game won state event handling
                elif self.state_manager.is_state(self.state_manager.GAME_WON):
                    running = self.state_manager.handle_game_won_input(event)
                    if not running:
                        break  # Exit the loop if we should quit
                    
                    # Only reset if we're continuing (R was pressed)
                    if self.state_manager.is_state(self.state_manager.PLAYING):
                        self.reset_game_state()
                        self.elapsed_time = 0  # Reset timer when restarting after winning
                
                # Level up state event handling
                elif self.state_manager.is_state(self.state_manager.LEVEL_UP):
                    option_rects = self.menu_system.draw_level_up(
                        self.player.level, self.state_manager.upgrade_options)
                    self.state_manager.handle_level_up_input(
                        event, self.menu_system, self.player.level, option_rects, self.ability_manager)
                
                # Main menu handling
                elif self.state_manager.is_state(self.state_manager.MAIN_MENU):
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.state_manager.change_state(self.state_manager.PLAYING)
                        self.elapsed_time = 0  # Reset timer when starting game from menu
                elif self.state_manager.is_state(self.state_manager.INPUTTING_NAME):
                    self.current_name, name_confirmed = self.state_manager.handle_name_input(event, current_name=self.current_name, max_length=10)

                    if name_confirmed and len(self.current_name) > 0:
                        # Save name to database
                        self.database.adicionar(self.current_name, int(self.elapsed_time))
                        self.current_input_name = ""
                        self.state_manager.change_state(self.state_manager.GAME_OVER)
                  
            # Handle test mode input
            self.handle_test_mode_input(events)
            
            # Update game state if playing
            if self.state_manager.is_state(self.state_manager.PLAYING):
                self.update_game_state()
                self.elapsed_time += self.clock.get_time() / 1000  # Update elapsed time
                
                # Check if game time limit is reached
                if self.elapsed_time >= GAME_TIME_LIMIT:
                    self.trigger_game_won()
                          
            # Render appropriate screen
            self.render_screen()
        
            # Control game frame rate
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
    
    def show_start_menu(self):
        """Display the start menu and wait for player to begin."""
        self.state_manager.change_state(self.state_manager.MAIN_MENU)
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                    self.state_manager.change_state(self.state_manager.PLAYING)
                    self.elapsed_time = 0  # Reset timer when starting from menu
            
            # Draw menu
            self.menu_system.draw_start_menu()
            pygame.display.flip()
            
            # Still need to tick the clock here to maintain frame rate
            self.clock.tick(FPS)
    
    def update_game_state(self):
        """Update all game logic."""
        # Get current keyboard state
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys)
        
        # Spawn enemies periodically
        self.enemy_manager.spawn_enemy(self.elapsed_time)
        
        # Update enemies
        self.enemy_manager.update(keys)
        
        # Handle player shooting
        self.projectile_manager.handle_auto_shooting(self.enemy_manager.enemies)
        
        # Update projectiles
        self.projectile_manager.update()
        
        # Check for collisions
        self.check_collisions()
        
        # Update all sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy_manager.enemies)
        self.all_sprites.add(self.projectile_manager.projectiles)
    
    def check_collisions(self):
        """Handle all collision detection and resolution."""
        # Projectile-Enemy Collisions
        killed_enemies = self.collision_manager.check_projectile_enemy_collisions(
            self.projectile_manager.projectiles, self.enemy_manager.enemies)
        
        # Enemy-Player Collisions
        collided_enemies, is_player_dead = self.collision_manager.check_enemy_player_collisions(
            self.enemy_manager.enemies)
        
        if is_player_dead:
            self.trigger_game_over()
    
    def render_screen(self):
        """Render appropriate screen based on game state."""
        if self.state_manager.is_state(self.state_manager.MAIN_MENU):
            # Menu screen
            self.menu_system.draw_start_menu()
        elif self.state_manager.is_state(self.state_manager.GAME_OVER):
            # Game over screen
            self.menu_system.draw_game_over(self.player.level)
        elif self.state_manager.is_state(self.state_manager.GAME_WON):
            # Game won screen
            self.menu_system.draw_game_won(self.player.level)
        elif self.state_manager.is_state(self.state_manager.LEVEL_UP):
            # Base game still visible under level up menu
            # Draw game first
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.hud.draw(int(self.elapsed_time))
            
            # Then draw level up overlay
            option_rects = self.menu_system.draw_level_up(
                self.player.level, self.state_manager.upgrade_options)
        else:
            # Normal game rendering
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.hud.draw(int(self.elapsed_time))
        
        # Update display
        pygame.display.flip()

def main():
    """Entry point for the game."""
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()