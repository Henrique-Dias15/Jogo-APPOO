import pygame
import sys
import random
from utils.settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.triangle_enemy import TriangleEnemy
from entities.square_enemy import SquareEnemy
from entities.triangle_enemy import TriangleEnemy
from entities.fast_enemy import FastEnemy
from entities.projectile import Projectile
from ui.hud import HUD
from ui.menu import MenuSystem
from abilities.ability_manager import AbilityManager

class GameController:
    """
    Primary game management class responsible for:
    - Game state management
    - Game loop control
    - Collision detection
    - Enemy and projectile spawning
    - Rendering game elements
    """
    def __init__(self):
        """
        Initialize the game with all necessary components.
        Sets up pygame, screen, game state, and system components.
        """
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
        
        # Initialize game state
        self.reset_game_state()
        
        # Connect player level up to game controller
        self.player.set_level_up_callback(self.trigger_level_up)
    
    def reset_game_state(self):
        """
        Reset all game variables to their initial state.
        Allows for clean game restart or initial setup.
        """
        # Sprite Groups for efficient rendering and collision detection
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Create player at screen center
        self.player = Player(self.width // 2, self.height // 2, screen_width=self.width, screen_height=self.height)
        self.all_sprites.add(self.player)
        
        # Create HUD for the player
        self.hud = HUD(self.player, self.screen)
        
        # Create ability manager
        self.ability_manager = AbilityManager(self.player)
        
        # Game state flags
        self.game_over_state = False
        self.game_won_state = False
        self.level_up_state = False
        self.upgrade_options = []
        
        # Timing and spawn management
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.elapsed_time = 0
        
        
    def trigger_level_up(self):
        """Pause game and show level up screen."""
        self.level_up_state = True
        self.upgrade_options = self.ability_manager.get_upgrade_options()
    
    def run(self):
        """
        Main game loop that manages different game states.
        Handles menu, gameplay, game over screens, and level up.
        """
        # Start with the main menu
        self.show_start_menu()
        
        running = True
        while running:
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Game over state event handling
                if self.game_over_state:
                    running = self.handle_game_over_events(event)
                    
                # Game won state event handling
                elif self.game_won_state:
                    running = self.handle_game_won_events(event)
                
                # Level up state event handling
                elif self.level_up_state:
                    self.handle_level_up_events(event)
            
             # Update game state if not in game over or level up
            if not self.game_over_state and not self.level_up_state and not self.game_won_state:
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
    
    def handle_level_up_events(self, event):
        """Process player input during level up screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            option_rects = self.menu_system.draw_level_up(self.player.level, self.upgrade_options)
            
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    # Apply the selected upgrade
                    ability_name = self.upgrade_options[i]['ability']
                    self.ability_manager.upgrade_ability(ability_name)
                    
                    # Resume game
                    self.level_up_state = False
                    break
    
    def show_start_menu(self):
        """
        Display the start menu and wait for player to begin.
        Blocks main game loop until player starts the game.
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
            
            # Draw menu
            self.menu_system.draw_start_menu()
            pygame.display.flip()
    
    def update_game_state(self):
        """
        Update all game logic:
        - Player movement
        - Enemy spawning
        - Projectile management
        - Collision detection
        """
        # Get current keyboard state
        keys = pygame.key.get_pressed()
        
        # Update all sprites
        self.all_sprites.update(keys)
        
        # Spawn enemies periodically
        self.spawn_enemies()
        
        # Handle player shooting
        self.handle_player_shooting()
        
        # Check for collisions
        self.check_collisions()
    
    def spawn_enemies(self):
        """
        Spawn enemies at regular intervals with random enemy types.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > SPAWN_INTERVAL:
            # Choose a random enemy type based on current difficulty
            enemy_types = [
                Enemy,           # Basic enemy - most common
                SquareEnemy,     # Tough enemy
                TriangleEnemy,   # Unpredictable enemy
                FastEnemy        # Quick enemy
            ]
            
            # You can adjust probabilities based on player level
            weights = [0.6, 0.2, 1, 0.1]  # 60% basic, 20% square, 10% triangle, 10% fast
            
            # Make the game more challenging as time goes on
            if self.elapsed_time > GAME_TIME_LIMIT * 0.2:  # After 20% of the game time
                weights = [0.5, 0.25, 0.15, 0.1]
            elif self.elapsed_time > GAME_TIME_LIMIT * 0.4:  # After 40% of the game time
                weights = [0.4, 0.3, 0.2, 0.1]
            elif self.elapsed_time > GAME_TIME_LIMIT * 0.6:  # After 60% of the game time
                weights = [0.3, 0.35, 0.25, 0.1]
            elif self.elapsed_time > GAME_TIME_LIMIT * 0.8:  # After 80% of the game time
                weights = [0.2, 0.4, 0.3, 0.1]
            elif self.elapsed_time > GAME_TIME_LIMIT * 0.9:  # After 90% of the game time
                weights = [0.1, 0.5, 0.3, 0.1]
                
            
            # Select enemy type based on weights
            import random
            enemy_class = random.choices(enemy_types, weights=weights)[0]
            
            # Create the selected enemy type
            enemy = enemy_class(self.player, screen_width=self.width, screen_height=self.height)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = current_time
    
    # Modify the handle_player_shooting method to pass player's damage to projectiles
    def handle_player_shooting(self):
        """
        Manage player's automatic projectile shooting.
        Targets the closest enemy when possible.
        """
        if self.player.can_shoot() and self.enemies:
            # Find the closest enemy to target
            closest_enemy = None
            min_distance = float('inf')
            
            for enemy in self.enemies:
                # Calculate distance between player and this enemy
                dx = enemy.rect.centerx - self.player.rect.centerx
                dy = enemy.rect.centery - self.player.rect.centery
                distance = (dx**2 + dy**2)**0.5  # Euclidean distance
                
                # Update closest enemy if this one is closer
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
            
            # Create projectile targeting the closest enemy
            projectile = Projectile(
                self.player.rect.centerx, 
                self.player.rect.centery,
                closest_enemy.rect.centerx, 
                closest_enemy.rect.centery,
                screen_width=self.width,  # Pass actual screen width
                screen_height=self.height,  # Pass actual screen height
                damage=self.player.projectile_damage  # Pass player's damage
            )
            
            self.projectiles.add(projectile)
            self.all_sprites.add(projectile)
            
            # Update last shot time
            self.player.last_shot = pygame.time.get_ticks()
    
    def check_collisions(self):
        """
        Detect and handle various game collisions:
        - Projectiles hitting enemies
        - Enemies hitting the player
        """
        # Projectile-Enemy Collisions
        for projectile in self.projectiles:
            hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies, False)
            for enemy in hit_enemies:
                if enemy.take_damage(projectile.damage):
                    # Enemy destroyed, give player experience
                    self.player.gain_exp(10)
                    enemy.kill()
                projectile.kill()
        
        # Enemy-Player Collisions
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(enemy, self.player):
                self.player.hp -= 10
                enemy.kill()
                
                if self.player.hp <= 0:
                    self.trigger_game_over()
    
    def trigger_game_over(self):
        """
        Set game over state and prepare for restart/exit.
        """
        self.game_over_state = True
        
        # Clear all game sprites
        self.all_sprites.empty()
        self.enemies.empty()
        self.projectiles.empty()
        
    def trigger_game_won(self):
        """
        Set game won state and prepare for restart/exit.
        """
        self.game_won_state = True
        
        # Clear all game sprites
        self.all_sprites.empty()
        self.enemies.empty()
        self.projectiles.empty()
    
    def handle_game_over_events(self, event):
        """
        Process player input during game over screen.
        Returns whether the game should continue running.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                self.reset_game_state()
                return True
            elif event.key == pygame.K_q:
                # Quit the game
                pygame.quit()
                sys.exit()
        return True
    
    def handle_game_won_events(self, event):
        """
        Process player input during game won screen.
        Returns whether the game should continue running.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                self.reset_game_state()
                return True
            elif event.key == pygame.K_q:
                # Quit the game
                pygame.quit()
                sys.exit()
        return True
    
    def render_screen(self):
        """
        Render appropriate screen based on game state.
        Handles game running, game over, and level up screens.
        """
        if self.game_over_state:
            # Game over screen
            self.menu_system.draw_game_over(self.player.level)
        elif self.game_won_state:
            # Game won screen
            self.menu_system.draw_game_won(self.player.level)
        elif self.level_up_state:
            # Base game still visible under level up menu
            # Draw game first
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.hud.draw(int(self.elapsed_time))
            
            # Then draw level up overlay
            option_rects = self.menu_system.draw_level_up(self.player.level, self.upgrade_options)
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