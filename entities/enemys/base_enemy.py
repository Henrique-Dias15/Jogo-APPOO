import pygame
import random
import math
from utils.settings import *
from entities.experience.experience import Experience
from entities.player.player import Player
from typing import Optional, Tuple
import math
class BaseEnemy(pygame.sprite.Sprite):
    """Base class for all enemies in the game."""

    def __init__(self, 
        player:Player, 
        size:Tuple[int, int, int], 
        color:Tuple[int, int, int], 
        speed:float, 
        hp:int, 
        shooter:bool, 
        damage:float, 
        x:Optional[float]=None, 
        y:Optional[float]=None, 
        screen_width:Optional[float]=None, 
        screen_height:Optional[float]=None, 
        spritesheet:Optional[str]=None, frame_ammount:Optional[int]=None, frame_delay:Optional[float]=None
    ) -> None:
        super().__init__()

        # Create enemy sprite with specified size and color
        if spritesheet:
            try:
                self.sheet = pygame.transform.scale(pygame.image.load(spritesheet).convert_alpha(), size)
                frame_width = self.sheet.get_width() // frame_ammount
                frame_height = self.sheet.get_height()
                self.run_frames = [
                    pygame.transform.scale(self.sheet.subsurface((i * frame_width, 0, frame_width, frame_height)), size)
                    for i in range(frame_ammount)
                ]
                self.current_frame = 0
                self.frame_timer = 0
                self.frame_delay = frame_delay  # Default to 100ms
                self.image = self.run_frames[0]
                if frame_ammount > 1:
                    self.has_animation = True
                else:
                    self.has_animation = False
            except Exception as e:
                print(f"Erro ao carregar spritesheet: {e}")
                self.image = pygame.Surface(size)
                self.image.fill(color)
                self.has_animation = False
        else:
            self.image = pygame.Surface(size)
            self.image.fill(color)
            self.has_animation = False

        # Reference to player for targeting
        self.player = player

        # Shooter flag
        self.shooter = shooter
        # Boss Flag
        self.is_boss = False 

        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT

        # Randomize spawn location if not specified
        self.speed = speed
        self.hp = hp
        self.damage = damage

        self.rect = self.image.get_rect()
        if x is None or y is None:
            self.spawn_at_screen_edge()
        else:
            self.rect.center = (x, y)
            
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.rect.center = (self.pos_x, self.pos_y)
        self.base_height = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)

    def spawn_at_screen_edge(self) -> None:
        """Spawn enemy at random edge of screen"""
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            self.rect.midtop = (random.randint(0, self.screen_width), 0)
        elif side == 'bottom':
            self.rect.midbottom = (random.randint(0, self.screen_width), self.screen_height)
        elif side == 'left':
            self.rect.midleft = (0, random.randint(0, self.screen_height))
        else:  # right
            self.rect.midright = (self.screen_width, random.randint(0, self.screen_height))

    def update(self, *args, **kwargs) -> Optional[int]:
        """Move enemy towards player, now accepts any arguments"""
            # Check for status effects that prevent movement
        if hasattr(self, 'frozen') and self.frozen:
            return 0
        
        # Handle charmed enemies (attack other enemies instead)
        if hasattr(self, 'charmed') and self.charmed:
            self.update_charmed_behavior()
            return 0
        
        # Calculate direction to player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        self.angle = math.degrees(math.atan2(-dy, dx))  # Adjust angle for pygame coordinate system
        
        # Normalize movement
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
        
        self.pos_x += dx * self.speed
        self.pos_y += dy * self.speed

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        self.rect.center = (self.pos_x, self.pos_y)

    def take_damage(self, damage) -> bool:
        """Handle enemy taking damage"""
        self.hp -= damage
        return self.hp <= 0

    def can_shoot(self) -> bool:
        """Check if the enemy can shoot based on cooldown"""
        if not self.shooter:
            return False
        return pygame.time.get_ticks() - self.last_shot > self.projectile_cooldown

    def kill(self, ammount) -> Experience:
        """Handle enemy death"""
        xp = Experience(self.player, self.rect.x, self.rect.y, ammount)
        super().kill()
        return xp
    
    def update_animation_rotation(self) -> None:
        if hasattr(self, 'has_animation') and self.has_animation:
            now = pygame.time.get_ticks()
            if now - self.frame_timer >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.frame_timer = now
                self.image = self.run_frames[self.current_frame]
        else:
            if self.angle is not None:
                center = self.rect.center
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.rect = self.image.get_rect(center=center)
            if hasattr(self, 'sheet') and self.sheet:
                self.image = self.run_frames[0]
                self.current_frame = 0
        if self.angle is not None:
            center = self.rect.center
            self.image = pygame.transform.rotate(self.run_frames[self.current_frame], self.angle+90)
            self.rect = self.image.get_rect(center=center)
        else:
            self.image = self.run_frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def update_animation_turning(self) -> None:
        if hasattr(self, 'has_animation') and self.has_animation:
            now = pygame.time.get_ticks()
            if now - self.frame_timer >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.frame_timer = now
                self.image = self.run_frames[self.current_frame]
        else:
            if hasattr(self, 'sheet') and self.sheet:
                self.image = self.run_frames[0]
                self.current_frame = 0
        if not (self.angle > 90 or self.angle < -90):  # Only flip if not facing left:
                    center = self.rect.center
                    self.image = pygame.transform.flip(self.run_frames[self.current_frame], True, False)
                    self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)

    def update_animation_turning_rotation(self) -> None:
        if hasattr(self, 'has_animation') and self.has_animation:
            now = pygame.time.get_ticks()
            if now - self.frame_timer >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.frame_timer = now
                self.image = self.run_frames[self.current_frame]
        
        frame = self.run_frames[self.current_frame]
        flip = False
        angle = self.angle if self.angle is not None else 0
        if self.angle is not None:
            if  -90 < self.angle < 90:
                flip = True

        if flip:
            frame = pygame.transform.flip(frame, True, False)
        else:
            angle = angle+180

        if self.angle is not None:
            frame = pygame.transform.rotate(frame, angle)

        center = self.rect.center
        self.image = frame
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)