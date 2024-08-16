from LereMontar.funcoesVerificar import Conexo, Bipartido, Euleriano, Cíclico
<<<<<<< HEAD
from LereMontar.funcoesListar import  ComponentesConexas, ComponentesFortementeConexas, listarVerticesArticulacao, listarArestasPonte, arvore_lexicografica, arvore_largura, arvore_geradora_minima, ordem_topologica, caminho_minimo
=======
from LereMontar.funcoesListar import  ComponentesConexas, ComponentesFortementeConexas, encontrar_vertices_articulacao, listarArestasPonte, arvore_lexicografica, arvore_largura, listarCaminhoEuleriano, arvore_geradora_minima, ordem_topologica, caminho_minimo, valor_fluxo_maximo, fecho_transitivo
>>>>>>> 9b9e95179cdd007fefbb38d0f7ae19658cac6d67


def mostrar_menu_principal():
    print("\nGrafo criado com sucesso! O que você deseja fazer agora?")
    print("1. Verificar")
    print("2. Listar")
    print("3. Gerar")
    print("0. Sair")

def mostrar_menu_verificar():
    print("\nVerificar:")
    print("a. Conexo")
    print("b. Bipartido")
    print("c. Euleriano")
    print("d. Possui ciclo")
    print("0. Voltar ao menu principal")

def mostrar_menu_listar():
    print("\nListar:")
    print("a. Componentes conexas")
    print("b. Componentes fortemente conexas")
    print("c. Uma trilha Euleriana")
    print("d. Vértices de articulação")
    print("e. Arestas ponte")
    print("0. Voltar ao menu principal")

def mostrar_menu_gerar():
    print("\nGerar:")
    print("a. Árvore de profundidade")
    print("b. Árvore de largura")
    print("c. Árvore geradora mínima")
    print("d. Ordenação topológica")
    print("e. Valor do caminho mínimo entre dois vérƟces")
    print("f. Valor do fluxo máximo")
    print("g. Fecho transitivo")
    print("0. Voltar ao menu principal")

def obter_escolha():
    escolha = input("Escolha uma opção: ").strip().lower()
    return escolha

def processar_escolha_principal(escolha, grafo):
    if escolha == '1':
        mostrar_menu_verificar()
        escolha_verificar = obter_escolha()
        processar_escolha_verificar(escolha_verificar, grafo)
    elif escolha == '2':
        mostrar_menu_listar()
        escolha_listar = obter_escolha()
        processar_escolha_listar(escolha_listar, grafo)
    elif escolha == '3':
        mostrar_menu_gerar()
        escolha_gerar = obter_escolha()
        processar_escolha_gerar(escolha_gerar, grafo)
    elif escolha == '0':
        print("Saindo...")
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

def processar_escolha_verificar(escolha, grafo):
    while escolha != '0':
        if escolha == 'a':
            print(Conexo(grafo))
        elif escolha == 'b':
            print(Bipartido(grafo))
        elif escolha == 'c':
            print(Euleriano(grafo))
        elif escolha == 'd':
            print(Cíclico(grafo))
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        escolha = obter_escolha()

def processar_escolha_listar(escolha, grafo):
    while escolha != '0':
        if escolha == 'a':
            print(ComponentesConexas(grafo))
        elif escolha == 'b':
            print(ComponentesFortementeConexas(grafo))
        elif escolha == 'c':
            print(listarCaminhoEuleriano(grafo))
        elif escolha == 'd':
            print(encontrar_vertices_articulacao(grafo))
        elif escolha == 'e':
            print(f"Arestas ponte: {listarArestasPonte(grafo)}")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        escolha = obter_escolha()

def processar_escolha_gerar(escolha, grafo):
    while escolha != '0':
        if escolha == 'a':
            print(arvore_lexicografica(grafo))
        elif escolha == 'b':
            print(arvore_largura(grafo))
        elif escolha == 'c':
            print(arvore_geradora_minima(grafo))
        elif escolha == 'd':
            print(ordem_topologica(grafo))
        elif escolha == 'e':
            print(caminho_minimo(grafo))
        elif escolha == 'f':
            print(valor_fluxo_maximo(grafo, 0, (len(grafo.vertices) - 1)))
        elif escolha == 'g':
            print(fecho_transitivo(grafo))
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        escolha = obter_escolha()
