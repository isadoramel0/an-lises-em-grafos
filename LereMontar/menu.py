from LereMontar.funcoesVerificar import quantVertices, quantArestas, Conexo, Bipartido, Euleriano, Hamiltoniano

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
    print("0. Sair")

def obter_escolha():
    escolha = input("Escolha uma opção: ").strip().lower()
    return escolha

def processar_escolha(escolha, grafo):
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
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

