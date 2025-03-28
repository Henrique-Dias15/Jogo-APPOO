import pygame
import random
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NÃO é copia do jogo do Matheus!")

clock = pygame.time.Clock()

# Player settings
PLAYER_SPEED = 300  # pixels per second
PLAYER_RADIUS = 15

# Enemy settings
ENEMY_SPEED = 100  # pixels per second
ENEMY_RADIUS = 10
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000)  # spawn enemy every 1000ms

# Define player
class Player:
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

        # Keep inside the screen bounds
        self.pos.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, self.pos.x))
        self.pos.y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, self.pos.y))
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), PLAYER_RADIUS)

# Define enemy
class Enemy:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
    
    def update(self, target_pos, dt):
        # Calculate direction vector toward the player
        direction = target_pos - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
        self.pos += direction * ENEMY_SPEED * dt
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), ENEMY_RADIUS)

def spawn_enemy():
    # Spawn at a random edge of the screen
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

def main():
    player = Player((WIDTH / 2, HEIGHT / 2))
    enemies = []
    running = True
    dt = 0
    
    while running:
        dt = clock.tick(60) / 1000  # Convert milliseconds to seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT:
                enemies.append(spawn_enemy())
        
        player.handle_input(dt)
        
        # Update enemies
        for enemy in enemies:
            enemy.update(player.pos, dt)
        
        # Collision detection (basic)
        for enemy in enemies[:]:
            if (enemy.pos - player.pos).length() < PLAYER_RADIUS + ENEMY_RADIUS:
                                # Game over: enter end game menu
                menu_running = True
                while menu_running:
                    # Define button rectangles
                    try_again_button = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 - 50, 200, 50)
                    quit_button = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 20, 200, 50)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            if try_again_button.collidepoint(mouse_pos):
                                main()  # Restart the game
                                return
                            elif quit_button.collidepoint(mouse_pos):
                                pygame.quit()
                                exit()

                    # Draw menu background and buttons
                    screen.fill((50, 50, 50))  # Dark grey background
                    pygame.draw.rect(screen, (0, 200, 0), try_again_button)
                    pygame.draw.rect(screen, (200, 0, 0), quit_button)

                    font = pygame.font.Font(None, 36)
                    text_try = font.render("Try Again", True, (255, 255, 255))
                    text_quit = font.render("Quit", True, (255, 255, 255))
                    screen.blit(text_try, (try_again_button.x + 35, try_again_button.y + 10))
                    screen.blit(text_quit, (quit_button.x + 70, quit_button.y + 10))

                    pygame.display.flip()
                    clock.tick(60)
        
        # Drawing
        screen.fill((0, 100, 0))  # dark green background
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()