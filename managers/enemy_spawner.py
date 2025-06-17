import pygame
import random
from ui import hud
from utils.settings import *
from entities.enemys.enemy import Enemy
from entities.enemys.square_enemy import SquareEnemy
from entities.enemys.triangle_enemy import TriangleEnemy
from entities.enemys.fast_enemy import FastEnemy
from entities.enemys.big_square import BigSquare

class EnemyManager:
    """
    Handles enemy spawning and management.
    """
    def __init__(self, player, screen_width, screen_height):
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.last_boss_spawn = 0
        self.is_boss_alive = False  # Track if a boss is currently alive
        self.enemies = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
    
    def spawn_enemy(self, elapsed_time):
        """
        Spawn enemies based on game time and difficulty progression.
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
            
            # Adjust probabilities based on game progression
            weights = [0.6, 0.2, 0.1, 0.1]  # 60% basic, 20% square, 10% triangle, 10% fast
            
            # Make the game more challenging as time goes on
            if elapsed_time > GAME_TIME_LIMIT * 0.2:  # After 20% of the game time
                weights = [0.5, 0.25, 0.15, 0.1]
            elif elapsed_time > GAME_TIME_LIMIT * 0.4:  # After 40% of the game time
                weights = [0.4, 0.3, 0.2, 0.1]
            elif elapsed_time > GAME_TIME_LIMIT * 0.6:  # After 60% of the game time
                weights = [0.3, 0.35, 0.25, 0.1]
            elif elapsed_time > GAME_TIME_LIMIT * 0.8:  # After 80% of the game time
                weights = [0.2, 0.4, 0.3, 0.1]
            elif elapsed_time > GAME_TIME_LIMIT * 0.9:  # After 90% of the game time
                weights = [0.1, 0.5, 0.3, 0.1]
                
            # Select enemy type based on weights
            enemy_class = random.choices(enemy_types, weights=weights)[0]
            # Create the selected enemy type
            enemy = enemy_class(self.player, screen_width=self.screen_width, screen_height=self.screen_height)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = current_time
            return enemy
        return None
    
    def spawn_boss(self, elapsed_time):
        """
            Spawn a boss if one is not alive, 5 minutes cooldown
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_boss_spawn > BOSS_SPAWN_INTERVAL and self.is_boss_alive == False:
            # Create a boss enemy
            boss = BigSquare(self.player, screen_width=self.screen_width, screen_height=self.screen_height)
            self.boss.add(boss)
            self.enemies.add(boss)
            self.all_sprites.add(boss)
            self.is_boss_alive = True
            return boss
        return None
    
    def kill_boss(self):
        """Reset boss spawn state"""
        self.last_boss_spawn = pygame.time.get_ticks()
        self.is_boss_alive = False
    
    def update(self, *args, **kwargs):
        """Update all enemies"""
        self.enemies.update(*args, **kwargs)
        
    def draw(self, screen):
        """Draw all enemies"""
        self.enemies.draw(screen)

    def draw_boss(self, screen, hud=None):
        """Draw the boss if it exists and its health bar"""
        if self.boss:
            self.boss.draw(screen)
            
            # Desenhe a barra de vida para cada boss
            if hud:
                for boss in self.boss:
                    hud.draw_boss_health_bar(boss)
    
    def reset(self):
        """Clear all enemies"""
        self.enemies.empty()
        self.all_sprites.empty()
        self.isBossAlive = False
        self.last_boss_spawn = 0