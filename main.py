import sys
from game_controller import main

if __name__ == "__main__":
    # Suporte para modo de teste de habilidade individual
    test_ability = None
    if len(sys.argv) > 1:
        test_ability = sys.argv[1]
        print(f"🧪 MODO TESTE: Carregando apenas a habilidade '{test_ability}'")
    
    main(test_ability=test_ability)