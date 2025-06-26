import pygame
import random
from utils.settings import PLAYER_SPEED, PLAYER_MAX_HP, ENEMY_SPEED
from abilities.base_ability import PassiveAbility, ActiveAbility, BuffAbility

# Import abilities by category
from abilities.passive import CatnipSpell, FrozenClaw, FlamingPaws, Tailwind, CleaningTongue, Pawquake, SteelWhiskers, StaticFur
from entities.player.player import Player
from managers.projectile_manager import ProjectileManager
from managers.enemy_spawner import EnemyManager
from entities.enemys.base_enemy import BaseEnemy
class AbilityManager:
    """
    Enhanced ability manager that handles magical cat abilities and upgrades.
    """
    def __init__(self, player: Player) -> None:
        self.player = player
        
        # Magical abilities collection
        self.passive_abilities = {
            # Passive abilities
            'catnip_spell': CatnipSpell(),
            'flaming_paws': FlamingPaws(),
            'frozen_claw': FrozenClaw(),
            'tailwind': Tailwind(),
            'cleaning_tongue': CleaningTongue(),
            'pawquake': Pawquake(),
            'steel_whiskers': SteelWhiskers(),
            'static_fur': StaticFur(),
        }
        
        # Player's acquired abilities
        self.player_abilities = {}
        
        # Auto-triggered abilities that need regular updates
        self.active_abilities = []
        
        # References for ability activation
        self.projectile_manager = None
        self.enemy_manager = None
    
    def set_managers(self, projectile_manager:ProjectileManager, enemy_manager:EnemyManager) -> None:
        """Set references to game managers for ability activation."""
        self.projectile_manager = projectile_manager
        self.enemy_manager = enemy_manager
    
    def update(self, dt, keys: pygame.key.ScancodeWrapper = None) -> None:
        """Update all active abilities and handle auto-triggers."""
        if not self.enemy_manager or not self.projectile_manager:
            return
        
        enemies = self.enemy_manager.enemies
        
        # Update all player abilities
        for ability in self.player_abilities.values():
            ability.update(dt, self.player, enemies, 
                         projectile_manager=self.projectile_manager)
        
        # Handle auto-triggered abilities
        for ability_name, ability in self.player_abilities.items():
            if hasattr(ability, 'should_auto_trigger') and ability.should_auto_trigger(self.player, enemies):
                self.activate_ability(ability_name, keys=keys)
        
        # Update enemy status effects
        self.update_enemy_effects(enemies)
    
    def update_enemy_effects(self, enemies:list[BaseEnemy]) -> None:
        """Update status effects on enemies."""
        current_time = pygame.time.get_ticks()
        
        for enemy in enemies:
            # Handle freeze
            if hasattr(enemy, 'frozen') and enemy.frozen:
                if current_time >= enemy.freeze_end_time:
                    enemy.frozen = False
                    enemy.speed = getattr(enemy, 'original_speed', ENEMY_SPEED)
            
            # Handle burning
            if hasattr(enemy, 'burning') and enemy.burning:
                if current_time >= enemy.burn_end_time:
                    enemy.burning = False
                    enemy.speed = getattr(enemy, 'original_speed', ENEMY_SPEED)  # Restore speed when burn ends
                else:
                    # Apply burn damage periodically
                    if not hasattr(enemy, 'last_burn_tick'):
                        enemy.last_burn_tick = current_time
                    elif current_time - enemy.last_burn_tick >= 500:  # Every 500ms (0.5 seconds)
                        if enemy.take_damage(enemy.burn_damage):
                            self.player.gain_exp(5)  # Give exp when enemy dies from burn
                            enemy.kill()
                        enemy.last_burn_tick = current_time
    
    def activate_ability(self, ability_name:str, **kwargs) -> bool:
        """Activate a specific ability."""
        if ability_name in self.player_abilities:
            ability = self.player_abilities[ability_name]
            enemies = self.enemy_manager.enemies if self.enemy_manager else []
            return ability.activate(
                self.player, 
                enemies=enemies,
                projectile_manager=self.projectile_manager,
                **kwargs
            )
        return False
    
    def get_upgrade_options(self) -> list[dict]:
        """
        Generate upgrade options for magical abilities.
        """
        options = []
        
        # Add magical abilities (new or upgrades)
        abilities_options = self.get_magical_ability_options()
        
        # Randomly select 3 options
        selected_options = random.sample(abilities_options, min(3, len(abilities_options)))
        
        return selected_options
    
    def get_magical_ability_options(self) -> list[dict]:
        """Get available magical ability options."""
        options = []
        
        # New abilities (not yet acquired)
        for ability_name, ability in self.passive_abilities.items():
            if ability_name not in self.player_abilities:
                options.append({
                    'name': ability.name,
                    'ability': ability_name,
                    'type': 'new_magical',
                    'description': ability.description
                })
        
        # Upgradeable abilities
        for ability_name, ability in self.player_abilities.items():
            if ability.level < ability.max_level:
                options.append({
                    'name': ability.name,
                    'ability': ability_name,
                    'type': 'upgrade_magical',
                    'description': f"{ability.description}",
                    'level': ability.level + 1
                })
        
        return options
    
    def upgrade_ability(self, ability_name:str) -> bool:
        """Apply the selected ability upgrade to the player."""
        # Find the ability in upgrade options to get its type
        upgrade_options = self.get_magical_ability_options()
        ability_info = None
        
        for option in upgrade_options:
            if option['ability'] == ability_name:
                ability_info = option
                break
        
        if not ability_info:
            return False
        
        ability_type = ability_info.get('type', 'stat')

        if ability_type == 'new_magical':
            return self.acquire_magical_ability(ability_name)
        elif ability_type == 'upgrade_magical':
            return self.upgrade_magical_ability(ability_name)
        
        return False
    
    def acquire_magical_ability(self, ability_name:str) -> bool:
        """Acquire a new magical ability."""
        if ability_name in self.passive_abilities and ability_name not in self.player_abilities:
            # Create a new instance of the ability
            ability_class = type(self.passive_abilities[ability_name])
            new_ability = ability_class()
            
            # Add to player abilities
            self.player_abilities[ability_name] = new_ability
            
            # Activate passive abilities immediately
            if isinstance(new_ability, PassiveAbility):
                new_ability.activate(self.player)
            
            return True
        return False
    
    def upgrade_magical_ability(self, ability_name:str) -> bool:
        """Upgrade an existing magical ability."""
        if ability_name in self.player_abilities:
            ability = self.player_abilities[ability_name]
            return ability.upgrade()
        return False