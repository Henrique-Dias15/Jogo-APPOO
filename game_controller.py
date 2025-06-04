import pygame
import sys
from utils.settings import *
from entities.player import Player
from ui.hud import HUD
from ui.menu import MenuSystem
from managers.ability_manager import AbilityManager
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
        
        # Connect managers to ability system
        self.ability_manager.set_managers(self.projectile_manager, self.enemy_manager)
        
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
        
    def setup_test_mode(self, test_ability):
        """Configura o jogo para testar apenas uma habilidade específica."""
        print(f"🧪 MODO TESTE ATIVO: {test_ability}")
        
        # Mapeamento de nomes amigáveis para chaves de habilidade
        ability_map = {
            # Passivas
            'catnip': 'catnip_spell',
            'frozen': 'frozen_claw',
            
            # Projéteis  
            'whisker': 'whisker_beam',
            'furball': 'arcane_fur_ball',
            'tail': 'elemental_tail',
            
            # Ativas
            'teleport': 'feline_teleport',
            'gaze': 'enchanted_gaze',
            'rats': 'ghost_rat_summoning',
            'shield': 'purring_shield',
            'reflex': 'reflex_aura',
            
            # Área
            'fish': 'ethereal_fish_rain',
            'meow': 'mystical_meow'
        }
        
        # Converte nome amigável para chave real se necessário
        if test_ability in ability_map:
            test_ability = ability_map[test_ability]
        
        # Adiciona flag para indicar modo de teste
        self.test_mode = True
        self.test_ability_key = test_ability
        
        print(f"✅ Modo de teste configurado para: {test_ability}")
        print("⌨️  Controles:")
        print("   WASD/Setas: Mover")
        print("   T: Ativar habilidade de teste")
        print("   ESC: Sair")
        
    def apply_test_mode_modifications(self):
        """Aplica as modificações necessárias para o modo de teste."""
        if not hasattr(self, 'test_mode') or not self.test_mode:
            return
            
        ability_manager = self.ability_manager
        test_key = self.test_ability_key
        
        # Limpa todas as habilidades
        ability_manager.player_abilities.clear()
        
        # Adiciona apenas a habilidade de teste
        if test_key in ability_manager.available_abilities:
            ability_class = type(ability_manager.available_abilities[test_key])
            new_ability = ability_class()
            
            # Adiciona ao jogador
            ability_manager.player_abilities[test_key] = new_ability
            
            # Se for passiva, ativa imediatamente
            from abilities.base_ability import PassiveAbility
            if isinstance(new_ability, PassiveAbility):
                new_ability.activate(self.player)
                print(f"✨ Habilidade passiva '{new_ability.name}' ativada!")
            else:
                print(f"⚡ Habilidade '{new_ability.name}' pronta! Use 'T' para ativar.")
                
            # Reduz cooldown para facilitar teste
            if hasattr(new_ability, 'cooldown'):
                original_cooldown = new_ability.cooldown
                new_ability.cooldown = max(original_cooldown // 3, 300)
                print(f"🔧 Cooldown reduzido: {original_cooldown}ms → {new_ability.cooldown}ms")
        else:
            print(f"❌ Habilidade '{test_key}' não encontrada!")
            
    def handle_test_mode_input(self, events):
        """Gerencia input específico do modo de teste."""
        if not hasattr(self, 'test_mode') or not self.test_mode:
            return
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:  # Tecla T para ativar habilidade
                    self.activate_test_ability()
                elif event.key == pygame.K_ESCAPE:  # ESC para sair
                    pygame.quit()
                    sys.exit()
                    
    def activate_test_ability(self):
        """Ativa a habilidade de teste."""
        if not hasattr(self, 'test_ability_key'):
            return
            
        ability_manager = self.ability_manager
        test_key = self.test_ability_key
        
        if test_key in ability_manager.player_abilities:
            ability = ability_manager.player_abilities[test_key]
            
            if ability.can_activate():
                activated = ability_manager.activate_ability(test_key)
                if activated:
                    print(f"🎯 '{ability.name}' ativada!")
                else:
                    print(f"❌ Falha ao ativar '{ability.name}'")
            else:
                remaining = (ability.last_activation + ability.cooldown - pygame.time.get_ticks()) / 1000
                print(f"⏳ Cooldown: {remaining:.1f}s restantes")
        else:
            print(f"❌ Habilidade '{test_key}' não encontrada!")

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
            events = pygame.event.get()
            for event in events:
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
        
        # Update ability system
        dt = self.clock.get_time()
        self.ability_manager.update(dt, keys)
        
        # Spawn enemies periodically
        self.enemy_manager.spawn_enemy(self.elapsed_time)
        
        # Update enemies
        self.enemy_manager.update(keys)
        
        # Handle player shooting
        self.projectile_manager.handle_auto_shooting(self.enemy_manager.enemies)
        
        # Update projectiles (pass enemies for homing projectiles)
        self.projectile_manager.update(self.enemy_manager.enemies)
        
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
            self.hud.draw(int(self.elapsed_time), self.ability_manager)
            
            # Then draw level up overlay
            option_rects = self.menu_system.draw_level_up(
                self.player.level, self.state_manager.upgrade_options)
        else:
            # Normal game rendering
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.hud.draw(int(self.elapsed_time), self.ability_manager)
        
        # Update display
        pygame.display.flip()

def main(test_ability=None):
    """Entry point for the game."""
    game = GameController()
    
    # Se estiver no modo de teste, configura apenas uma habilidade
    if test_ability:
        game.setup_test_mode(test_ability)
        game.apply_test_mode_modifications()  # Apply modifications after setup
    
    game.run()

if __name__ == "__main__":
    main()