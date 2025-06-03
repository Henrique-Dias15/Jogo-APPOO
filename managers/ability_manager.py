from utils.settings import PLAYER_SPEED, PLAYER_MAX_HP

class AbilityManager:
    """
    Manages player abilities and upgrades, providing options during level up.
    """
    def __init__(self, player):
        self.player = player
        
        # Track ability levels
        self.abilities = {
            'damage': 1,
            'speed': 1,
            'health': 1
        }
    
    def get_upgrade_options(self):
        """
        Generate a list of available upgrades for the player to choose from.
        Returns a list of dictionaries with name and ability information.
        """
        return [
            {'name': 'More Damage', 'ability': 'damage', 'description': 'Increase your attack damage'},
            {'name': 'More Speed', 'ability': 'speed', 'description': 'Increase your movement speed'},
            {'name': 'More Health', 'ability': 'health', 'description': 'Increase your maximum health'}
        ]
    
    def upgrade_ability(self, ability_name):
        """Apply the selected ability upgrade to the player."""
        if ability_name not in self.abilities:
            return False
            
        # Increase the ability level
        self.abilities[ability_name] += 1
        
        # Apply the effect based on the ability
        if ability_name == 'damage':
            # Increase projectile damage
            self.player.projectile_damage = 10 + (self.abilities['damage'] * 5)
            
        elif ability_name == 'speed':
            # Increase movement speed
            self.player.speed = PLAYER_SPEED + (self.abilities['speed'] - 1)
            
        elif ability_name == 'health':
            # Increase max health
            old_max_hp = self.player.max_hp
            self.player.max_hp = PLAYER_MAX_HP + ((self.abilities['health'] - 1) * 20)
            # Also heal the player by the difference
            self.player.hp += (self.player.max_hp - old_max_hp)
            
        return True