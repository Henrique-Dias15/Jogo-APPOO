import pygame
import random
import sys  # Add this import
from utils.settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Magical Cat Game")
        self.clock = pygame.time.Clock()
        
        # Font for game over text
        self.font = pygame.font.Font(None, 36)
        
        # Game state
        self.game_over_state = False
        
        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)
        
        # Enemy spawn timer
        self.last_enemy_spawn = pygame.time.get_ticks()

    def spawn_enemy(self):
        """Spawn an enemy periodically"""
        if self.game_over_state:
            return
        
        now = pygame.time.get_ticks()
        if now - self.last_enemy_spawn > SPAWN_INTERVAL:
            enemy = Enemy(self.player)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = now

    def handle_player_shooting(self):
        """Handle automatic player shooting"""
        if self.game_over_state:
            return
        
        if self.player.can_shoot() and self.enemies:
            target = random.choice(list(self.enemies.sprites()))
            projectile = Projectile(
                self.player.rect.centerx, 
                self.player.rect.centery,
                target.rect.centerx, 
                target.rect.centery
            )
            self.projectiles.add(projectile)
            self.all_sprites.add(projectile)
            self.player.last_shot = pygame.time.get_ticks()

    def handle_collisions(self):
        """Check and handle collisions"""
        if self.game_over_state:
            return
        
        # Projectile hits enemy
        for projectile in self.projectiles:
            hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies, False)
            for enemy in hit_enemies:
                if enemy.take_damage(projectile.damage):
                    self.player.gain_exp(10)  # Gain exp for killing enemy
                    enemy.kill()
                projectile.kill()

        # Enemy hits player
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(enemy, self.player):
                self.player.hp -= 10
                enemy.kill()
                if self.player.hp <= 0:
                    self.game_over()

    def game_over(self):
        """Handle game over state"""
        print("Game Over!")
        self.game_over_state = True
        
        # Clear existing sprites
        self.all_sprites.empty()
        self.enemies.empty()
        self.projectiles.empty()

    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        # Game Over Text
        game_over_text = self.font.render("Game Over!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final Score Text
        score_text = self.font.render(f"Final Level: {self.player.level}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(score_text, score_rect)
        
        # Restart Prompt
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)

    def restart_game(self):
        """Restart the game"""
        self.__init__()  # Reinitialize the game state
        self.game_over_state = False

    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle game over state input
                if self.game_over_state:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_q:
                            running = False

            # Get pressed keys
            keys = pygame.key.get_pressed()

            # Update game state
            if not self.game_over_state:
                self.all_sprites.update(keys)
                self.spawn_enemy()
                self.handle_player_shooting()
                self.handle_collisions()

            # Draw
            if not self.game_over_state:
                self.screen.fill(BLACK)
                self.all_sprites.draw(self.screen)
            else:
                self.draw_game_over()

            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()  # Ensure complete exit

def main():
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()