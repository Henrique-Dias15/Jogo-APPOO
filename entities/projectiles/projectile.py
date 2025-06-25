import pygame
import math
from utils.settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, screen_width=None, screen_height=None, speed=7, damage=10, modifications=None, is_player_projectile=True, angle=None):
        super().__init__()
        
        # Store modifications and apply them
        self.modifications = modifications or {}
        self.is_player_projectile = is_player_projectile
        # Apply modifications to get final properties
        size = self.modifications.get('size', (5, 5))
        color = self.modifications.get('color', BLUE)
        self.angle = angle
        if 'spritesheet' in self.modifications:
            spritesheet_path = self.modifications['spritesheet']
            try:
                sheet = pygame.image.load(spritesheet_path).convert_alpha()
                frame_width = sheet.get_width() // 6
                frame_height = sheet.get_height()
                self.run_frames = [
                    pygame.transform.scale(sheet.subsurface((i * frame_width, 0, frame_width, frame_height)), (40, 40))
                    for i in range(6)
                ]
                self.current_frame = 0
                self.frame_timer = 0
                self.frame_delay = self.modifications.get('sprite_frame_delay')  # Default to 100ms
                if self.angle is not None:
                    self.image = pygame.transform.rotate(self.run_frames[0], self.angle)
                else:
                    self.image = self.run_frames[0]
                self.has_animation = True
            except Exception as e:
                print(f"Erro ao carregar spritesheet: {e}")
                self.image = pygame.Surface(size)
                self.image.fill(color)
                self.has_animation = False
        else:
            try:
                sheet = pygame.image.load('assets/images/abilities/base/Base.png').convert_alpha()
                frame_width = sheet.get_width() // 6
                frame_height = sheet.get_height()
                self.run_frames = [
                    pygame.transform.scale(sheet.subsurface((i * frame_width, 0, frame_width, frame_height)), (20, 20))
                    for i in range(6)
                ]
                self.current_frame = 0
                self.frame_timer = 0
                self.frame_delay = self.modifications.get('sprite_frame_delay')  # Default to 100ms
                if self.angle is not None:
                    self.image = pygame.transform.rotate(self.run_frames[0], self.angle)
                else:
                    self.image = self.run_frames[0]
                self.has_animation = True
            except Exception as e:
                print(f"Erro ao carregar spritesheet: {e}")
                self.image = pygame.Surface(size)
                self.image.fill(color)
                self.has_animation = False

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx, self.dy = 0, 0
        
        self.damage = damage

    def update(self, *args, **kwargs):
        """Move projectile, now accepts any arguments"""
        self.rect.x += self.dx
        self.rect.y += self.dy

        if hasattr(self, 'has_animation') and self.has_animation:
            now = pygame.time.get_ticks()
            if self.frame_delay is not None and now - self.frame_timer >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.frame_timer = now

                current_frame = self.run_frames[self.current_frame]
                if self.angle is not None:
                    center = self.rect.center
                    self.image = pygame.transform.rotate(current_frame, self.angle)
                    self.rect = self.image.get_rect(center=center)
                else:
                    self.image = current_frame
        # Remove if out of screen
        if (self.rect.right < 0 or self.rect.left > self.screen_width or
            self.rect.bottom < 0 or self.rect.top > self.screen_height):
            self.kill()