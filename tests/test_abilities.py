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
    'flaming': {
        'key': 'flaming_paws',
        'name': 'Patas Flamejantes',
        'description': 'Ataques causam queimadura e projéteis deixam rastro de fogo',
        'type': '🔮 Passiva'
    }
}

def show_menu():
    """Exibe o menu interativo de seleção"""
    print("\n🐱 Testador de Habilidades")
    print("-" * 30)
    
    # Organiza por categorias
    categories = {
        'Passivas': ['catnip', 'frozen', 'flaming']
    }
    
    choice_map = {}
    counter = 1
    
    for category, ability_keys in categories.items():
        print(f"\n{category}:")
        for key in ability_keys:
            ability = ABILITIES[key]
            print(f"  {counter}. {ability['name']}")
            choice_map[counter] = key
            counter += 1
    
    print(f"\n  {counter}. Testar todas")
    choice_map[counter] = 'all'
    
    print("  0. Sair")
    
    while True:
        try:
            choice = input("\nEscolha: ").strip()
            if choice == '0':
                return None
            
            choice = int(choice)
            if choice in choice_map:
                return choice_map[choice]
            else:
                print("Número inválido.")
        except ValueError:
            print("Digite um número válido.")

def test_ability(ability_key):
    """Testa uma habilidade específica"""
    if ability_key not in ABILITIES:
        print(f"Habilidade '{ability_key}' não encontrada!")
        return
    
    ability = ABILITIES[ability_key]
    print(f"\nTestando: {ability['name']}")
    print("Controles: WASD + T (ativar) + ESC (sair)")
    
    try:
        # Executa o jogo com a habilidade específica
        result = subprocess.run([
            'python3', 'main.py', ability_key
        ], cwd='/home/henrique/Jogo-APPOO')
        
        if result.returncode == 0:
            print(f"Teste concluído!")
        else:
            print(f"Erro durante o teste")
    except KeyboardInterrupt:
        print(f"\nTeste interrompido")
    except Exception as e:
        print(f"Erro: {e}")

def test_all_abilities():
    """Testa todas as habilidades sequencialmente"""
    print("\nTestando todas as habilidades...")
    
    for i, (key, ability) in enumerate(ABILITIES.items(), 1):
        print(f"\n[{i}/{len(ABILITIES)}] {ability['name']}")
        input("Enter para continuar...")
        test_ability(key)
    
    print("\nTodos os testes concluídos!")

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
                print("\nSaindo...")
                break
            elif choice == 'all':
                test_all_abilities()
            else:
                test_ability(choice)
                input("\nEnter para voltar ao menu...")
    
    except KeyboardInterrupt:
        print("\n\nTestador encerrado.")

if __name__ == "__main__":
    main()
