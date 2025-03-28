import pygame
import sys
import random
from utils.settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from ui.hud import HUD
from ui.menu import MenuSystem

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
        pygame.display.set_caption("Magical Cat Game")
        
        # Screen and timing setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # UI Systems
        self.menu_system = MenuSystem(self.screen)
        
        # Initialize game state
        self.reset_game_state()
    
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
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Create HUD for the player
        self.hud = HUD(self.player, self.screen)
        
        # Game state flags
        self.game_over_state = False
        
        # Timing and spawn management
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.score = 0
    
    def run(self):
        """
        Main game loop that manages different game states.
        Handles menu, gameplay, and game over screens.
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
            
            # Update game state if not in game over
            if not self.game_over_state:
                self.update_game_state()
                self.score += self.clock.get_time() / 1000  # Score based on survival time
            
            # Render appropriate screen
            self.render_screen()
            
            # Control game frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
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
        Spawn enemies at regular intervals.
        Randomizes enemy spawning to create dynamic challenge.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > SPAWN_INTERVAL:
            enemy = Enemy(self.player)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = current_time
    
    def handle_player_shooting(self):
        """
        Manage player's automatic projectile shooting.
        Targets random enemies when possible.
        """
        if self.player.can_shoot() and self.enemies:
            # Select a random enemy to target
            target = random.choice(list(self.enemies.sprites()))
            
            projectile = Projectile(
                self.player.rect.centerx, 
                self.player.rect.centery,
                target.rect.centerx, 
                target.rect.centery
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
                return False
        return True
    
    def render_screen(self):
        """
        Render appropriate screen based on game state.
        Handles game running and game over screens.
        """
        if not self.game_over_state:
            # Normal game rendering
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.hud.draw()
        else:
            # Game over screen
            self.menu_system.draw_game_over(self.player.level)
        
        # Update display
        pygame.display.flip()

def main():
    """Entry point for the game."""
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()