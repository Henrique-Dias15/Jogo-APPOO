import pygame
from utils.settings import *
from typing import Optional, Callable
class Player(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, screen_width: Optional[float]=None, screen_height: Optional[float]=None)->None:
        super().__init__()
        # Imagem parada
        self.stand_image = pygame.transform.scale(
            pygame.image.load('assets/images/kitty/Gatinho.png').convert_alpha(), (100, 100)
        )
        # Carrega frames do spritesheet (2 colunas)
        sheet = pygame.image.load('assets/images/kitty/Gatinho Correndo.png').convert_alpha()
        frame_width = sheet.get_width() // 2
        frame_height = sheet.get_height()
        self.run_frames = [
            pygame.transform.scale(sheet.subsurface((i * frame_width, 0, frame_width, frame_height)), (100, 100))
            for i in range(2)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 150  # ms por frame
        self.facing_right = True
        self.image = self.stand_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player attributes
        self.speed = PLAYER_SPEED
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_MAX_HP
        self.level = 1
        self.exp = 0
        self.projectile_cooldown = 500  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.level_up_callback = None  # Add callback for level up
        self.projectile_damage = 10  # Base projectile damage
        self.last_hit_time = 0  # Track last hit time for invincibility
        # Store actual screen dimensions
        self.screen_width = screen_width if screen_width is not None else SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else SCREEN_HEIGHT
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, keys:pygame.key.ScancodeWrapper) -> None:
        """Move the player based on keyboard input"""
        dx, dy = 0, 0
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.facing_right = True
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
            moving = True
        
        # Diagonal movement normalization
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        # Update position
        self.rect.x += int(dx)
        self.rect.y += int(dy)
        
        # Apply boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

        self.update_animation(moving)

    def gain_exp(self, amount:int) -> None:
        """Add experience points and check for level up"""
        self.exp += amount
        if self.exp >= 100:  # Simple level up mechanism
            self.level_up()

    def level_up(self) -> None:
        """Handle leveling up logic"""
        self.level += 1
        self.exp -= 100  # Reset exp
        self.hp = min(self.hp + 10, self.max_hp)
        
        # Notify game controller that we've leveled up
        if self.level_up_callback:
            self.level_up_callback()

    def set_level_up_callback(self, callback:Callable[[], None]) -> None:
        """Set the function to call when player levels up"""
        self.level_up_callback = callback

    def can_shoot(self) -> bool:
        """Check if player can shoot a projectile"""
        now = pygame.time.get_ticks()
        return now - self.last_shot > self.projectile_cooldown

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Update player state"""
        self.move(keys)

    def update_animation(self, moving:bool) -> None:
        now = pygame.time.get_ticks()
        if moving:
            if now - self.frame_timer > self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.frame_timer = now
            frame = self.run_frames[self.current_frame]
            if self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
            self.image = frame
        else:
            self.image = self.stand_image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
