from LereMontar.funcoesVerificar import quantVertices, quantArestas, Conexo, Bipartido, Euleriano, Hamiltoniano, Cíclico, Planar

def mostrar_menu():
    print("\nGrafo criado com sucesso! O que você deseja fazer agora?")
    print("1. Verificar")
    print("  a. Quantidade de vértices")
    print("  b. Quantidade de arestas")
    print("  c. Conexo")
    print("  d. Bipartido")
    print("  e. Euleriano")
    print("  f. Hamiltoniano")
    print("  g. Cíclico")
    print("  h. Planar")
    print("  0. Sair")

def obter_escolha():
    escolha = input("Escolha uma opção: ").strip().lower()
    return escolha

def processar_escolha(escolha, grafo):
    while escolha != '0':
        if escolha == 'a':
            print(f"Quantidade de vértices: {quantVertices(grafo)}")
        elif escolha == 'b':
            print(f"Quantidade de arestas: {quantArestas(grafo)}")
        elif escolha == 'c':
            print(f"O grafo {Conexo(grafo)} conexo")
        elif escolha == 'd':
            print(f"O grafo {Bipartido(grafo)}")
        elif escolha == 'e':
            print(f"O grafo {Euleriano(grafo)}")
        elif escolha == 'f':
            print(f"O grafo {Hamiltoniano(grafo)}")
        elif escolha == 'g':
            print(f"O grafo {Cíclico(grafo)}")
        elif escolha == 'h':
            print(f"O grafo {Planar(grafo)}")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        escolha = obter_escolha()
    

