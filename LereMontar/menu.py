from LereMontar.funcoesVerificar import Conexo, Bipartido, Euleriano, Cíclico
from LereMontar.funcoesListar import  listarComponentesConexas, listarCaminhoEuleriano, listarVerticesArticulacao, listarArestasPonte
# from LereMontar.funcoesGerar import gerarMatrizAdjacencia, gerarListaAdjacencia, gerarArvoreProfundidade, gerarArvoreLargura, gerarArvoreGeradoraMinima, gerarOrdemTopologica, gerarCaminhoMinimo, gerarFluxoMaximo, gerarFechamentoTransitivo

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
    print("d. Cíclico")
    print("0. Voltar ao menu principal")

def mostrar_menu_listar():
    print("\nListar:")
    print("a. Vértices")
    print("b. Arestas")
    print("c. Componentes conexas")
    print("d. Um caminho Euleriano")
    print("e. Um caminho Hamiltoniano")
    print("f. Vértices de articulação")
    print("g. Arestas ponte")
    print("0. Voltar ao menu principal")

def mostrar_menu_gerar():
    print("\nGerar:")
    print("a. Matriz de adjacência")
    print("b. Lista de adjacência")
    print("c. Árvore de profundidade")
    print("d. Árvore de largura")
    print("e. Árvore geradora mínima")
    print("f. Ordem topológica")
    print("g. Caminho mínimo entre dois vértices")
    print("h. Fluxo máximo")
    print("i. Fechamento transitivo")
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
            print(f"Componentes conexas: {listarComponentesConexas(grafo)}")
        elif escolha == 'b':
            print(f"Componentes fortemente conexas: {listarComponentesConexas(grafo)}")
        elif escolha == 'c':
            print(f"Caminho Euleriano: {listarCaminhoEuleriano(grafo)}")
        elif escolha == 'd':
            print(f"Vértices de articulação: {listarVerticesArticulacao(grafo)}")
        elif escolha == 'e':
            print(f"Arestas ponte: {listarArestasPonte(grafo)}")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        escolha = obter_escolha()

def processar_escolha_gerar(escolha, grafo):
    while escolha != '0':
        if escolha == 'a':
            print(f"Matriz de adjacência: {gerarMatrizAdjacencia(grafo)}")
        elif escolha == 'b':
            print(f"Lista de adjacência: {gerarListaAdjacencia(grafo)}")
        elif escolha == 'c':
            print(f"Árvore de profundidade: {gerarArvoreProfundidade(grafo)}")
        elif escolha == 'd':
            print(f"Árvore de largura: {gerarArvoreLargura(grafo)}")
        elif escolha == 'e':
            print(f"Árvore geradora mínima: {gerarArvoreGeradoraMinima(grafo)}")
        elif escolha == 'f':
            print(f"Ordem topológica: {gerarOrdemTopologica(grafo)}")
        elif escolha == 'g':
            print(f"Caminho mínimo entre dois vértices: {gerarCaminhoMinimo(grafo)}")
        elif escolha == 'h':
            print(f"Fluxo máximo: {gerarFluxoMaximo(grafo)}")
        elif escolha == 'i':
            print(f"Fechamento transitivo: {gerarFechamentoTransitivo(grafo)}")
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
        escolha = obter_escolha()
