#!/usr/bin/env python3
"""
🐱 Testador Rápido de Habilidades Mágicas 🐱

Script para testar habilidades individuais facilmente.
"""

import subprocess
import sys

# Mapeamento de habilidades disponíveis
ABILITIES = {
    # Passivas
    'catnip': {
        'key': 'catnip_spell',
        'name': 'Feitiço de Catnip',
        'description': 'Aumenta o poder mágico permanentemente',
        'type': '🔮 Passiva'
    },
    'frozen': {
        'key': 'frozen_claw', 
        'name': 'Garra Gélida',
        'description': 'Ataques têm chance de congelar inimigos',
        'type': '🔮 Passiva'
    },
    
    # Projéteis
    'whisker': {
        'key': 'whisker_beam',
        'name': 'Raio de Bigodes', 
        'description': 'Dispara feixes mágicos que atravessam inimigos',
        'type': '🎯 Projétil'
    },
    'furball': {
        'key': 'arcane_fur_ball',
        'name': 'Bola de Pêlo Arcana',
        'description': 'Lança esferas explosivas de pelos mágicos', 
        'type': '🎯 Projétil'
    },
    'tail': {
        'key': 'elemental_tail',
        'name': 'Cauda Elemental',
        'description': 'Dispara energia elemental com efeitos variados',
        'type': '🎯 Projétil'
    },
    
    # Ativas
    'teleport': {
        'key': 'feline_teleport',
        'name': 'Teleporte Felino',
        'description': 'Teleporta para uma posição segura',
        'type': '⚡ Ativa'
    },
    'gaze': {
        'key': 'enchanted_gaze',
        'name': 'Olhar Encantado',
        'description': 'Converte inimigos próximos em aliados temporários',
        'type': '⚡ Ativa'
    },
    'rats': {
        'key': 'ghost_rat_summoning',
        'name': 'Invocação de Ratos Fantasmas',
        'description': 'Invoca ratos espectrais que caçam inimigos',
        'type': '⚡ Ativa'
    },
    'shield': {
        'key': 'purring_shield',
        'name': 'Escudo de Ronronar',
        'description': 'Cria uma barreira que reflete dano aos inimigos',
        'type': '⚡ Buff'
    },
    'reflex': {
        'key': 'reflex_aura',
        'name': 'Aura de Reflexos',
        'description': 'Aumenta drasticamente a velocidade de ataque',
        'type': '⚡ Buff'
    },
    
    # Área de Efeito
    'fish': {
        'key': 'ethereal_fish_rain',
        'name': 'Chuva de Peixes Etéreos',
        'description': 'Invoca peixes mágicos que caem do céu',
        'type': '💫 Área'
    },
    'meow': {
        'key': 'mystical_meow',
        'name': 'Miau Místico',
        'description': 'Atordoa inimigos próximos temporariamente',
        'type': '💫 Área'
    }
}

def show_menu():
    """Exibe o menu interativo de seleção"""
    print("\n" + "="*80)
    print("🐱 TESTADOR DE HABILIDADES MÁGICAS 🐱")
    print("="*80)
    
    # Organiza por categorias
    categories = {
        '🔮 Habilidades Passivas': ['catnip', 'frozen'],
        '🎯 Habilidades de Projétil': ['whisker', 'furball', 'tail'],
        '⚡ Habilidades Ativas': ['teleport', 'gaze', 'rats', 'shield', 'reflex'],
        '💫 Habilidades de Área': ['fish', 'meow']
    }
    
    choice_map = {}
    counter = 1
    
    for category, ability_keys in categories.items():
        print(f"\n{category}:")
        for key in ability_keys:
            ability = ABILITIES[key]
            print(f"  {counter:2d}. {ability['name']}")
            print(f"      {ability['description']}")
            choice_map[counter] = key
            counter += 1
    
    print(f"\n  {counter:2d}. Testar TODAS as habilidades (sequencial)")
    choice_map[counter] = 'all'
    
    print(f"\n   0. Sair")
    print("="*80)
    
    while True:
        try:
            choice = input("\n🎮 Digite o número da habilidade: ").strip()
            if choice == '0':
                return None
            
            choice = int(choice)
            if choice in choice_map:
                return choice_map[choice]
            else:
                print("❌ Número inválido. Tente novamente.")
        except ValueError:
            print("❌ Digite um número válido.")

def test_ability(ability_key):
    """Testa uma habilidade específica"""
    if ability_key not in ABILITIES:
        print(f"❌ Habilidade '{ability_key}' não encontrada!")
        return
    
    ability = ABILITIES[ability_key]
    print(f"\n🧪 Testando: {ability['name']} ({ability['type']})")
    print(f"📝 {ability['description']}")
    print("\n⌨️  Controles do Teste:")
    print("   WASD/Setas: Mover o gato")
    print("   T: Ativar habilidade")
    print("   ESC: Sair do teste")
    print("\n🎮 Iniciando jogo...")
    
    try:
        # Executa o jogo com a habilidade específica
        result = subprocess.run([
            'python3', 'main.py', ability_key
        ], cwd='/home/henrique/Jogo-APPOO')
        
        if result.returncode == 0:
            print(f"✅ Teste de '{ability['name']}' concluído!")
        else:
            print(f"❌ Erro durante o teste de '{ability['name']}'")
    except KeyboardInterrupt:
        print(f"\n🛑 Teste de '{ability['name']}' interrompido")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_all_abilities():
    """Testa todas as habilidades sequencialmente"""
    print("\n🔄 Testando TODAS as habilidades sequencialmente...")
    print("🛑 Pressione ESC em cada teste para passar para a próxima habilidade")
    
    for i, (key, ability) in enumerate(ABILITIES.items(), 1):
        print(f"\n📊 Progresso: {i}/{len(ABILITIES)}")
        input(f"▶️  Pressione Enter para testar '{ability['name']}'...")
        test_ability(key)
        print(f"✅ Teste {i} de {len(ABILITIES)} concluído")
    
    print("\n🎉 Todos os testes concluídos!")

def show_help():
    """Exibe ajuda do script"""
    print("🐱 Testador de Habilidades Mágicas")
    print("="*40)
    print("Uso:")
    print("  python3 test_abilities_menu.py          # Menu interativo")
    print("  python3 test_abilities_menu.py <nome>   # Teste direto")
    print("  python3 test_abilities_menu.py all      # Teste todas")
    print("\nHabilidades disponíveis:")
    for key, ability in ABILITIES.items():
        print(f"  {key:10} - {ability['name']}")

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        # Modo linha de comando
        ability_key = sys.argv[1].lower()
        
        if ability_key == 'help' or ability_key == '--help':
            show_help()
            return
        elif ability_key == 'all':
            test_all_abilities()
            return
        elif ability_key in ABILITIES:
            test_ability(ability_key)
            return
        else:
            print(f"❌ Habilidade '{ability_key}' não encontrada!")
            show_help()
            return
    
    # Modo interativo
    try:
        while True:
            choice = show_menu()
            
            if choice is None:
                print("\n👋 Saindo do testador. Até logo!")
                break
            elif choice == 'all':
                test_all_abilities()
            else:
                test_ability(choice)
                input("\n⏸️  Pressione Enter para voltar ao menu...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Testador encerrado. Até logo!")

if __name__ == "__main__":
    main()
