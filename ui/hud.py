import pygame
from utils.settings import *

class HUD:
    """Manages the heads-up display for game information."""
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw(self, clock, ability_manager=None):
        """Render all HUD elements."""
        self._draw_health_bar()
        self._draw_level_and_exp()
        self._draw_time(clock)
        if ability_manager:
            self._draw_active_abilities(ability_manager)
    
    def _draw_health_bar(self):
        """Draw player's health bar."""
        bar_width = 200
        bar_height = 20
        fill_width = int((self.player.hp / self.player.max_hp) * bar_width)
        
        # Outline
        pygame.draw.rect(self.screen, WHITE, 
            (10, 10, bar_width, bar_height), 2)
        
        # Fill
        pygame.draw.rect(self.screen, RED, 
            (10, 10, fill_width, bar_height))
    
    def _draw_level_and_exp(self):
        """Display player's level and experience."""
        level_text = self.font.render(
            f"Level: {self.player.level}", 
            True, WHITE
        )
        exp_text = self.font.render(
            f"EXP: {self.player.exp}/100", 
            True, WHITE
        )
        
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(exp_text, (10, 70))
    
    def _draw_time(self, clock):
        """Display the current game time in minutes:seconds format."""
        # Convert to minutes and seconds
        minutes = int(clock) // 60
        seconds = int(clock) % 60
        
        time_text = self.font.render(
            f"Time: {minutes:02d}:{seconds:02d}", 
            True, WHITE
        )
        
        self.screen.blit(time_text, (10, 100))
    
    def _draw_active_abilities(self, ability_manager):
        """Display active abilities and their status."""
        y_offset = 140
        
        # Show acquired abilities
        if ability_manager.player_abilities:
            abilities_text = self.small_font.render("Habilidades Ativas:", True, WHITE)
            self.screen.blit(abilities_text, (10, y_offset))
            y_offset += 25
            
            for ability_name, ability in ability_manager.player_abilities.items():
                # Show ability name and level
                ability_text = f"{ability.name} (Nv.{ability.level})"
                if ability.is_active:
                    ability_text += " [ATIVO]"
                    color = GREEN
                elif not ability.can_activate():
                    # Show cooldown
                    remaining_cooldown = (ability.cooldown - (pygame.time.get_ticks() - ability.last_used)) / 1000
                    ability_text += f" ({remaining_cooldown:.1f}s)"
                    color = RED
                else:
                    color = WHITE
                
                text_surface = self.small_font.render(ability_text, True, color)
                self.screen.blit(text_surface, (10, y_offset))
                y_offset += 20
        
        # Show shield status
        if hasattr(self.player, 'has_purring_shield') and self.player.has_purring_shield:
            shield_text = self.small_font.render("ESCUDO ATIVO", True, CYAN)
            self.screen.blit(shield_text, (10, y_offset))