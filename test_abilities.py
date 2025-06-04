#!/usr/bin/env python3
"""
Sistema de Teste Individual de Habilidades
Permite testar uma habilidade por vez para debugging e validação.
"""

import pygame
import sys
from game_controller import GameController

# Lista de todas as habilidades disponíveis para teste
AVAILABLE_ABILITIES = {
    # Passivas
    'catnip_spell': 'Feitiço de Catnip (Passiva)',
    'frozen_claw': 'Garra Gélida (Passiva)',
    
    # Projéteis
    'whisker_beam': 'Raio de Bigodes (Projétil)',
    'arcane_fur_ball': 'Bola de Pêlo Arcana (Projétil)',
    'elemental_tail': 'Cauda Elemental (Projétil)',
    
    # Ativas
    'feline_teleport': 'Teleporte Felino (Ativo)',
    'enchanted_gaze': 'Olhar Encantado (Ativo)',
    'ghost_rat_summoning': 'Invocação de Ratos Fantasmas (Ativo)',
    'purring_shield': 'Escudo de Ronronar (Buff)',
    'reflex_aura': 'Aura de Reflexos (Buff)',
    
    # Área de Efeito
    'ethereal_fish_rain': 'Chuva de Peixes Etéreos (Área)',
    'mystical_meow': 'Miau Místico (Área)'
}

class AbilityTester:
    def __init__(self):
        self.selected_ability = None
        self.game = None
    
    def show_menu(self):
        """Mostra o menu de seleção de habilidades"""
        print("\n" + "="*60)
        print("🐱 TESTADOR DE HABILIDADES MÁGICAS 🐱")
        print("="*60)
        print("Selecione uma habilidade para testar:")
        print()
        
        abilities_list = list(AVAILABLE_ABILITIES.items())
        for i, (key, description) in enumerate(abilities_list, 1):
            print(f"{i:2d}. {description}")
        
        print()
        print(" 0. Sair")
        print("="*60)
        
        while True:
            try:
                choice = input("Digite o número da habilidade: ").strip()
                if choice == '0':
                    return None
                
                choice = int(choice)
                if 1 <= choice <= len(abilities_list):
                    selected_key = abilities_list[choice - 1][0]
                    selected_desc = abilities_list[choice - 1][1]
                    print(f"\n✅ Selecionado: {selected_desc}")
                    return selected_key
                else:
                    print("❌ Número inválido. Tente novamente.")
            except ValueError:
                print("❌ Digite um número válido.")
    
    def setup_test_game(self, ability_key):
        """Configura o jogo com apenas uma habilidade ativa"""
        print(f"\n🎮 Iniciando teste da habilidade: {AVAILABLE_ABILITIES[ability_key]}")
        print("⌨️  Controles:")
        print("   WASD ou Setas: Mover")
        print("   Espaço: Ativar habilidade (se aplicável)")
        print("   ESC: Voltar ao menu")
        print("\n🔄 Iniciando jogo em 3 segundos...")
        
        # Pequena pausa para o usuário ler
        import time
        time.sleep(3)
        
        # Cria o jogo
        self.game = GameController()
        
        # Modifica o ability_manager para ter apenas a habilidade selecionada
        self.modify_ability_manager(ability_key)
        
        # Inicia o jogo
        self.game.run()
    
    def modify_ability_manager(self, ability_key):
        """Modifica o ability manager para ter apenas uma habilidade"""
        ability_manager = self.game.ability_manager
        
        # Limpa todas as habilidades existentes
        ability_manager.player_abilities.clear()
        
        # Adiciona apenas a habilidade selecionada
        if ability_key in ability_manager.available_abilities:
            ability_class = type(ability_manager.available_abilities[ability_key])
            new_ability = ability_class()
            ability_manager.player_abilities[ability_key] = new_ability
            
            # Se for passiva, ativa imediatamente
            from abilities.base_ability import PassiveAbility
            if isinstance(new_ability, PassiveAbility):
                new_ability.activate(self.game.player)
                print(f"✨ Habilidade passiva '{new_ability.name}' ativada automaticamente!")
            else:
                print(f"⚡ Habilidade '{new_ability.name}' adicionada! Use Espaço para ativar.")
            
            # Para habilidades de projétil, dá algumas melhorias para facilitar o teste
            if 'projectile' in ability_key or 'beam' in ability_key or 'ball' in ability_key:
                # Reduz o cooldown para teste mais rápido
                new_ability.cooldown = max(new_ability.cooldown // 3, 500)
                print(f"🔧 Cooldown reduzido para {new_ability.cooldown}ms para facilitar o teste")
        
        # Adiciona tecla especial para ativar habilidades manualmente
        self.setup_manual_activation()
    
    def setup_manual_activation(self):
        """Configura ativação manual de habilidades com Espaço"""
        original_handle_input = self.game.handle_input
        
        def enhanced_handle_input(events):
            # Chama o input original
            original_handle_input(events)
            
            # Adiciona ativação manual com Espaço
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.activate_test_ability()
        
        self.game.handle_input = enhanced_handle_input
    
    def activate_test_ability(self):
        """Ativa manualmente a habilidade de teste"""
        ability_manager = self.game.ability_manager
        
        for ability_name, ability in ability_manager.player_abilities.items():
            # Tenta ativar a habilidade
            activated = ability_manager.activate_ability(ability_name)
            if activated:
                print(f"🎯 Habilidade '{ability.name}' ativada!")
            else:
                if not ability.can_activate():
                    remaining = (ability.last_activation + ability.cooldown - pygame.time.get_ticks()) / 1000
                    print(f"⏳ Cooldown: {remaining:.1f}s restantes")
                else:
                    print(f"❌ Não foi possível ativar '{ability.name}'")
    
    def run(self):
        """Executa o testador de habilidades"""
        print("🚀 Iniciando Testador de Habilidades...")
        
        while True:
            ability_key = self.show_menu()
            
            if ability_key is None:
                print("\n👋 Saindo do testador. Até logo!")
                break
            
            try:
                self.setup_test_game(ability_key)
                # Quando o jogo termina, volta para o menu
                print(f"\n✅ Teste da habilidade '{AVAILABLE_ABILITIES[ability_key]}' concluído!")
                input("Pressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n🛑 Teste interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro durante o teste: {e}")
                input("Pressione Enter para continuar...")

def main():
    """Função principal do testador"""
    try:
        tester = AbilityTester()
        tester.run()
    except KeyboardInterrupt:
        print("\n\n👋 Testador encerrado. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        print("Por favor, verifique se o jogo está funcionando corretamente.")

if __name__ == "__main__":
    main()
