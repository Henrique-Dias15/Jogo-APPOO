#!/usr/bin/env python3
"""
Script simples para testar uma habilidade específica.
Uso: python3 test_single_ability.py <nome_da_habilidade>
"""

import sys
import subprocess

# Mapeamento de habilidades
ABILITIES = {
    # Passivas
    'catnip': 'catnip_spell',
    'frozen': 'frozen_claw',
    
    # Projéteis  
    'whisker': 'whisker_beam',
    'furball': 'arcane_fur_ball',
    'tail': 'elemental_tail',
    
    # Ativas
    'teleport': 'feline_teleport',
    'gaze': 'enchanted_gaze',
    'rats': 'ghost_rat_summoning',
    'shield': 'purring_shield',
    'reflex': 'reflex_aura',
    
    # Área
    'fish': 'ethereal_fish_rain',
    'meow': 'mystical_meow'
}

def show_help():
    """Mostra a ajuda do script"""
    print("🐱 Testador Rápido de Habilidades")
    print("=" * 40)
    print("Uso: python3 test_single_ability.py <habilidade>")
    print("\nHabilidades disponíveis:")
    
    categories = {
        "Passivas": ['catnip', 'frozen'],
        "Projéteis": ['whisker', 'furball', 'tail'], 
        "Ativas": ['teleport', 'gaze', 'rats', 'shield', 'reflex'],
        "Área": ['fish', 'meow']
    }
    
    for category, abilities in categories.items():
        print(f"\n{category}:")
        for ability in abilities:
            print(f"  {ability}")
    
    print("\nExemplo: python3 test_single_ability.py whisker")

def create_test_config(ability_key):
    """Cria arquivo de configuração temporário para teste"""
    config_content = f'''# Configuração temporária para teste da habilidade: {ability_key}
TEST_MODE = True
TEST_ABILITY = "{ability_key}"
ENABLE_ALL_ABILITIES = False
'''
    
    with open('/home/henrique/Jogo-APPOO/test_config.py', 'w') as f:
        f.write(config_content)

def modify_ability_manager_for_test(ability_key):
    """Cria uma versão modificada do ability_manager para teste"""
    
    # Lê o ability_manager original
    with open('/home/henrique/Jogo-APPOO/managers/ability_manager.py', 'r') as f:
        original_content = f.read()
    
    # Cria backup
    with open('/home/henrique/Jogo-APPOO/managers/ability_manager_backup.py', 'w') as f:
        f.write(original_content)
    
    # Modifica o __init__ para incluir apenas a habilidade de teste
    modified_content = original_content.replace(
        '# Magical abilities collection',
        f'''# Magical abilities collection (MODO TESTE - apenas {ability_key})
        print(f"🧪 MODO TESTE: Carregando apenas '{ability_key}'")'''
    )
    
    # Substitui o dicionário de habilidades
    ability_dict_start = modified_content.find("self.available_abilities = {")
    ability_dict_end = modified_content.find("}", ability_dict_start) + 1
    
    if ability_dict_start != -1 and ability_dict_end != -1:
        # Cria novo dicionário com apenas a habilidade selecionada
        from abilities.passive import CatnipSpell, FrozenClaw
        from abilities.projectile import WhiskerBeam, ArcaneFurBall, ElementalTail
        from abilities.active import FelineTeleport, EnchantedGaze, GhostRatSummoning, PurringShield, ReflexAura
        from abilities.area_effect import EtherealFishRain, MysticalMeow
        
        ability_classes = {
            'catnip_spell': 'CatnipSpell',
            'frozen_claw': 'FrozenClaw',
            'whisker_beam': 'WhiskerBeam',
            'arcane_fur_ball': 'ArcaneFurBall',
            'elemental_tail': 'ElementalTail',
            'feline_teleport': 'FelineTeleport',
            'enchanted_gaze': 'EnchantedGaze',
            'ghost_rat_summoning': 'GhostRatSummoning',
            'purring_shield': 'PurringShield',
            'reflex_aura': 'ReflexAura',
            'ethereal_fish_rain': 'EtherealFishRain',
            'mystical_meow': 'MysticalMeow'
        }
        
        if ability_key in ability_classes:
            new_dict = f"self.available_abilities = {{\n            '{ability_key}': {ability_classes[ability_key]}()\n        }}"
            modified_content = (modified_content[:ability_dict_start] + 
                              new_dict + 
                              modified_content[ability_dict_end:])
    
    # Salva o arquivo modificado
    with open('/home/henrique/Jogo-APPOO/managers/ability_manager.py', 'w') as f:
        f.write(modified_content)

def restore_ability_manager():
    """Restaura o ability_manager original"""
    try:
        with open('/home/henrique/Jogo-APPOO/managers/ability_manager_backup.py', 'r') as f:
            original_content = f.read()
        
        with open('/home/henrique/Jogo-APPOO/managers/ability_manager.py', 'w') as f:
            f.write(original_content)
        
        # Remove arquivos temporários
        import os
        os.remove('/home/henrique/Jogo-APPOO/managers/ability_manager_backup.py')
        if os.path.exists('/home/henrique/Jogo-APPOO/test_config.py'):
            os.remove('/home/henrique/Jogo-APPOO/test_config.py')
        
        print("✅ Arquivo original restaurado!")
    except Exception as e:
        print(f"❌ Erro ao restaurar: {e}")

def main():
    if len(sys.argv) != 2:
        show_help()
        return
    
    ability_name = sys.argv[1].lower()
    
    if ability_name not in ABILITIES:
        print(f"❌ Habilidade '{ability_name}' não encontrada!")
        show_help()
        return
    
    ability_key = ABILITIES[ability_name]
    
    try:
        print(f"🧪 Preparando teste da habilidade: {ability_key}")
        
        # Cria configuração de teste
        create_test_config(ability_key)
        
        # Modifica ability_manager
        modify_ability_manager_for_test(ability_key)
        
        print(f"🎮 Iniciando jogo com apenas '{ability_key}' ativa...")
        print("⌨️  Use WASD para mover e Espaço para ativar habilidades")
        print("🛑 Pressione Ctrl+C para sair e restaurar")
        
        # Executa o jogo
        subprocess.run(['python3', '/home/henrique/Jogo-APPOO/main.py'])
        
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        # Sempre restaura o arquivo original
        restore_ability_manager()

if __name__ == "__main__":
    main()
