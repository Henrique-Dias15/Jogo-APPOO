import pygame
import random
from utils.settings import PLAYER_SPEED, PLAYER_MAX_HP, ENEMY_SPEED
from abilities.base_ability import PassiveAbility, ActiveAbility, BuffAbility

# Import abilities by category
from abilities.passive import CatnipSpell, FrozenClaw, FlamingPaws
from abilities.projectile import WhiskerBeam, ArcaneFurBall, ElementalTail
from abilities.active import (
    FelineTeleport, EnchantedGaze, GhostRatSummoning, 
    PurringShield, ReflexAura
)
from abilities.area_effect import EtherealFishRain, MysticalMeow

class AbilityManager:
    """
    Enhanced ability manager that handles magical cat abilities and upgrades.
    """
    def __init__(self, player):
        self.player = player
        
        # Traditional stat abilities
        self.stat_abilities = {
            'damage': 1,
            'speed': 1,
            'health': 1
        }
        
        # Magical abilities collection
        self.available_abilities = {
            'catnip_spell': CatnipSpell(),
            'flaming_paws': FlamingPaws(),
            'whisker_beam': WhiskerBeam(),
            'purring_shield': PurringShield(),
            'feline_teleport': FelineTeleport(),
            'arcane_fur_ball': ArcaneFurBall(),
            'ethereal_fish_rain': EtherealFishRain(),
            'frozen_claw': FrozenClaw(),
            'mystical_meow': MysticalMeow(),
            'enchanted_gaze': EnchantedGaze(),
            'reflex_aura': ReflexAura(),
            'elemental_tail': ElementalTail(),
            'ghost_rat_summoning': GhostRatSummoning()
        }
        
        # Player's acquired abilities
        self.player_abilities = {}
        
        # Auto-triggered abilities that need regular updates
        self.active_abilities = []
        
        # References for ability activation
        self.projectile_manager = None
        self.enemy_manager = None
    
    def set_managers(self, projectile_manager, enemy_manager):
        """Set references to game managers for ability activation."""
        self.projectile_manager = projectile_manager
        self.enemy_manager = enemy_manager
    
    def update(self, dt, keys=None):
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
    
    def update_enemy_effects(self, enemies):
        """Update status effects on enemies."""
        current_time = pygame.time.get_ticks()
        
        for enemy in enemies:
            # Handle stun
            if hasattr(enemy, 'stunned') and enemy.stunned:
                if current_time >= enemy.stun_end_time:
                    enemy.stunned = False
                    enemy.speed = getattr(enemy, 'original_speed', ENEMY_SPEED)
            
            # Handle charm
            if hasattr(enemy, 'charmed') and enemy.charmed:
                if current_time >= enemy.charm_end_time:
                    enemy.charmed = False
                    if hasattr(enemy, 'original_color'):
                        enemy.image.fill(enemy.original_color)
            
            # Handle freeze
            if hasattr(enemy, 'frozen') and enemy.frozen:
                if current_time >= enemy.freeze_end_time:
                    enemy.frozen = False
                    enemy.speed = getattr(enemy, 'original_speed', ENEMY_SPEED)
            
            # Handle burning
            if hasattr(enemy, 'burning') and enemy.burning:
                if current_time >= enemy.burn_end_time:
                    enemy.burning = False
                else:
                    # Apply burn damage periodically
                    if not hasattr(enemy, 'last_burn_tick'):
                        enemy.last_burn_tick = current_time
                    elif current_time - enemy.last_burn_tick >= 1000:  # Every second
                        enemy.take_damage(enemy.burn_damage)
                        enemy.last_burn_tick = current_time
    
    def activate_ability(self, ability_name, **kwargs):
        """Activate a specific ability."""
        if ability_name in self.player_abilities:
            ability = self.player_abilities[ability_name]
            return ability.activate(
                self.player, 
                enemies=self.enemy_manager.enemies,
                projectile_manager=self.projectile_manager,
                **kwargs
            )
        return False
    
    def get_upgrade_options(self):
        """
        Generate upgrade options including both traditional stats and magical abilities.
        """
        options = []
        
        # Traditional stat upgrades (always available)
        stat_options = [
            {'name': 'Mais Dano', 'ability': 'damage', 'type': 'stat',
             'description': 'Aumenta o dano dos ataques básicos'},
            {'name': 'Mais Velocidade', 'ability': 'speed', 'type': 'stat',
             'description': 'Aumenta a velocidade de movimento'},
            {'name': 'Mais Vida', 'ability': 'health', 'type': 'stat',
             'description': 'Aumenta a vida máxima'}
        ]
        
        # Add magical abilities (new or upgrades)
        magical_options = self.get_magical_ability_options()
        
        # Combine and randomly select 3 options
        all_options = stat_options + magical_options
        selected_options = random.sample(all_options, min(3, len(all_options)))
        
        return selected_options
    
    def get_magical_ability_options(self):
        """Get available magical ability options."""
        options = []
        
        # New abilities (not yet acquired)
        for ability_name, ability in self.available_abilities.items():
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
                    'name': f"{ability.name} (Nível {ability.level + 1})",
                    'ability': ability_name,
                    'type': 'upgrade_magical',
                    'description': f"Melhora: {ability.description}"
                })
        
        return options
    
    
    def upgrade_ability(self, ability_name):
        """Apply the selected ability upgrade to the player."""
        # Find the ability in upgrade options to get its type
        upgrade_options = self.get_upgrade_options()
        ability_info = None
        
        for option in upgrade_options:
            if option['ability'] == ability_name:
                ability_info = option
                break
        
        if not ability_info:
            return False
        
        ability_type = ability_info.get('type', 'stat')
        
        if ability_type == 'stat':
            return self.upgrade_stat_ability(ability_name)
        elif ability_type == 'new_magical':
            return self.acquire_magical_ability(ability_name)
        elif ability_type == 'upgrade_magical':
            return self.upgrade_magical_ability(ability_name)
        
        return False
    
    def upgrade_stat_ability(self, ability_name):
        """Upgrade traditional stat abilities."""
        if ability_name not in self.stat_abilities:
            return False
            
        # Increase the ability level
        self.stat_abilities[ability_name] += 1
        
        # Apply the effect based on the ability
        if ability_name == 'damage':
            # Increase projectile damage
            self.player.projectile_damage = 10 + (self.stat_abilities['damage'] * 5)
            
        elif ability_name == 'speed':
            # Increase movement speed
            self.player.speed = PLAYER_SPEED + (self.stat_abilities['speed'] - 1)
            
        elif ability_name == 'health':
            # Increase max health
            old_max_hp = self.player.max_hp
            self.player.max_hp = PLAYER_MAX_HP + ((self.stat_abilities['health'] - 1) * 20)
            # Also heal the player by the difference
            self.player.hp += (self.player.max_hp - old_max_hp)
            
        return True
    
    def acquire_magical_ability(self, ability_name):
        """Acquire a new magical ability."""
        if ability_name in self.available_abilities and ability_name not in self.player_abilities:
            # Create a new instance of the ability
            ability_class = type(self.available_abilities[ability_name])
            new_ability = ability_class()
            
            # Add to player abilities
            self.player_abilities[ability_name] = new_ability
            
            # Activate passive abilities immediately
            if isinstance(new_ability, PassiveAbility):
                new_ability.activate(self.player)
            
            return True
        return False
    
    def upgrade_magical_ability(self, ability_name):
        """Upgrade an existing magical ability."""
        if ability_name in self.player_abilities:
            ability = self.player_abilities[ability_name]
            return ability.upgrade()
        return False