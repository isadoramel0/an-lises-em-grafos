from LereMontar.funcoesVerificar import quantVertices, quantArestas, Conexo, Bipartido, Euleriano, Hamiltoniano, Cíclico, Planar
from LereMontar.funcoesListar import listarVertices, listarArestas, listarComponentesConexas #, listarCaminhoEuleriano, listarCaminhoHamiltoniano, listarVerticesArticulacao, listarArestasPonte
# from LereMontar.funcoesGerar import gerarMatrizAdjacencia, gerarListaAdjacencia, gerarArvoreProfundidade, gerarArvoreLargura, gerarArvoreGeradoraMinima, gerarOrdemTopologica, gerarCaminhoMinimo, gerarFluxoMaximo, gerarFechamentoTransitivo

def mostrar_menu_principal():
    print("\nGrafo criado com sucesso! O que você deseja fazer agora?")
    print("1. Verificar")
    print("2. Listar")
    print("3. Gerar")
    print("0. Sair")

def mostrar_menu_verificar():
    print("\nVerificar:")
    print("a. Quantidade de vértices")
    print("b. Quantidade de arestas")
    print("c. Conexo")
    print("d. Bipartido")
    print("e. Euleriano")
    print("f. Hamiltoniano")
    print("g. Cíclico")
    print("h. Planar")
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

def processar_escolha_listar(escolha, grafo):
    while escolha != '0':
        if escolha == 'a':
            print(f"Vértices: {listarVertices(grafo)}")
        elif escolha == 'b':
            print(f"Arestas: {listarArestas(grafo)}")
        elif escolha == 'c':
            print(f"Componentes conexas: {listarComponentesConexas(grafo)}")
        elif escolha == 'd':
            print(f"Caminho Euleriano: {listarCaminhoEuleriano(grafo)}")
        elif escolha == 'e':
            print(f"Caminho Hamiltoniano: {listarCaminhoHamiltoniano(grafo)}")
        elif escolha == 'f':
            print(f"Vértices de articulação: {listarVerticesArticulacao(grafo)}")
        elif escolha == 'g':
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
