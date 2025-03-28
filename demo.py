import pygame
import random
import math

pygame.init()

# =========================
# Configuration
# =========================
FULLSCREEN = True

if FULLSCREEN:
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("VS - First Experiments")
clock = pygame.time.Clock()

# Colors (RGB)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
DARK_GREY = (50, 50, 50)
BLACK = (0, 0, 0)

# Constants for player and enemy
PLAYER_SPEED = 300  # pixels per second
PLAYER_RADIUS = 15

ENEMY_SPEED = 100  # pixels per second
ENEMY_RADIUS = 10

# Event for enemy spawn
SPAWN_EVENT = pygame.USEREVENT + 1

# =========================
# Preload Fonts (for performance)
# =========================
FONT_TITLE = pygame.font.Font(None, 48)
FONT_INSTR = pygame.font.Font(None, 36)
FONT_HUD   = pygame.font.Font(None, 36)
FONT_BUTTON = pygame.font.Font(None, 36)

# =========================
# Game Classes
# =========================

class Player:
    """Class representing the player."""
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
    
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movement.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movement.y += 1
        if movement.length_squared() > 0:
            movement = movement.normalize() * PLAYER_SPEED * dt
            self.pos += movement

        # Restrict movement within the screen boundaries
        self.pos.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, self.pos.x))
        self.pos.y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, self.pos.y))
    
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), PLAYER_RADIUS)


class Enemy:
    """Class representing an enemy."""
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
    
    def update(self, target_pos, dt):
        # Calculate direction towards the player
        direction = target_pos - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
        self.pos += direction * ENEMY_SPEED * dt
    
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.pos.x), int(self.pos.y)), ENEMY_RADIUS)


def spawn_enemy():
    """Spawn an enemy at a random position along the screen edge."""
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x = random.randint(0, WIDTH)
        y = 0
    elif side == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT
    elif side == 'left':
        x = 0
        y = random.randint(0, HEIGHT)
    else:
        x = WIDTH
        y = random.randint(0, HEIGHT)
    return Enemy((x, y))

# =========================
# State Functions
# =========================

def run_main_menu():
    """Display the main menu and wait for player interaction."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                return "PLAYING"
        
        screen.fill(BLACK)
        title_text = FONT_TITLE.render("VS - First Experiments", True, WHITE)
        instr_text = FONT_INSTR.render("Press any key to start", True, WHITE)
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2,
                                 HEIGHT / 2 - title_text.get_height()))
        screen.blit(instr_text, (WIDTH / 2 - instr_text.get_width() / 2,
                                 HEIGHT / 2 + 10))
        pygame.display.flip()
        clock.tick(60)


def run_game():
    """
    Active game state.
    Returns a tuple (new_state, score) – for example, ("GAME_OVER", score) or ("QUIT", score)
    """
    # Initialize player, enemy list, and score
    player = Player((WIDTH / 2, HEIGHT / 2))
    enemies = []
    score = 0
    pygame.time.set_timer(SPAWN_EVENT, 1000)  # Activate spawn timer

    running = True
    while running:
        dt = clock.tick(240) / 1000  # dt in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", score
            elif event.type == SPAWN_EVENT:
                enemies.append(spawn_enemy())
        
        # Update player and enemies
        player.handle_input(dt)
        for enemy in enemies:
            enemy.update(player.pos, dt)
        
        # Check collisions (basic)
        for enemy in enemies:
            if (enemy.pos - player.pos).length() < PLAYER_RADIUS + ENEMY_RADIUS:
                pygame.time.set_timer(SPAWN_EVENT, 0)  # Deactivate spawn timer
                return "GAME_OVER", score
        
        # Update score (based on survival time)
        score += dt
        
        # Draw everything on the screen
        screen.fill(DARK_GREEN)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        
        # Draw the HUD (score)
        score_text = FONT_HUD.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
    
    return "QUIT", score


def run_game_over(score):
    """
    Display the game over screen with the final score.
    Returns the next state: "PLAYING" to restart or "QUIT" to exit.
    """
    # Define rectangles for the buttons
    try_again_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 50)
    quit_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 20, 200, 50)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if try_again_button.collidepoint(mouse_pos):
                    return "PLAYING"
                elif quit_button.collidepoint(mouse_pos):
                    return "QUIT"
        
        # Draw the game over screen
        screen.fill(DARK_GREY)
        title_text = FONT_TITLE.render("Game Over", True, WHITE)
        score_text = FONT_BUTTON.render(f"Score: {int(score)}", True, WHITE)
        
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - 150))
        screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - 100))
        
        # Draw buttons
        pygame.draw.rect(screen, GREEN, try_again_button)
        pygame.draw.rect(screen, RED, quit_button)
        text_try = FONT_BUTTON.render("Try Again", True, WHITE)
        text_quit = FONT_BUTTON.render("Quit", True, WHITE)
        screen.blit(text_try, (try_again_button.x + 35, try_again_button.y + 10))
        screen.blit(text_quit, (quit_button.x + 70, quit_button.y + 10))
        
        pygame.display.flip()
        clock.tick(60)

# =========================
# Main Loop with State Machine
# =========================

def main():
    state = "MAIN_MENU"
    score = 0
    while state != "QUIT":
        if state == "MAIN_MENU":
            state = run_main_menu()
        elif state == "PLAYING":
            state, score = run_game()
        elif state == "GAME_OVER":
            state = run_game_over(score)
    
    pygame.quit()

if __name__ == "__main__":
    main()
