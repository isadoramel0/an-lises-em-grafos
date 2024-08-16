from collections import defaultdict, deque
import heapq

class Vertice:
    def __init__(self, id):
        self.id = id
        self.cor = 'branco'
        self.pai = None
        self.tempo_descoberta = None
        self.tempo_finalizacao = None

class Grafo:
    def __init__(self, vertices, arestas, direcionado=False):
        self.vertices =  {v: Vertice(v) for v in vertices}
        self.arestas = arestas
        self.direcionado = direcionado
        self.adj_list = {v: [] for v in vertices}
        
        for (idAresta, v1, v2, peso) in arestas:
            if peso is not None:  # Grafo ponderado
                self.adj_list[v1].append((idAresta, v2, peso))
                if not self.direcionado:
                    self.adj_list[v2].append((idAresta, v1, peso))  # Aresta bidirecional
            else:  # Grafo não ponderado
                self.adj_list[v1].append(idAresta, v2)
                if not self.direcionado:
                    self.adj_list[v2].append(idAresta, v1)  # Aresta bidirecional

                    


def DFS(grafo, v, adj_list, visitados):
    visitados.add(v)
    vertice = grafo.vertices[v]
    vertice.cor = 'cinza'

    for vizinho in adj_list[v]:
        if isinstance(vizinho, tuple):
            vizinho_id = vizinho[1]  # Acessa o vértice destino na tupla (idAresta, vizinho, peso)
        else:
            vizinho_id = vizinho

        if vizinho_id not in visitados:
            DFS(grafo, vizinho_id, adj_list, visitados)

    vertice.cor = 'preto'


# ----- Funções Verificar -----

# ------- Conexo
def Conexo(grafo):
    # Se o grafo é direcionado, criamos uma lista de adjacência temporária com arestas bidirecionais
    if grafo.direcionado:
        adj_listTemp = {v: [] for v in grafo.vertices}
        for v in grafo.adj_list:
            for aresta in grafo.adj_list[v]:
                if isinstance(aresta, tuple):
                    vizinho = aresta[1]
                    adj_listTemp[v].append(vizinho) # Adiciona a aresta original
                    adj_listTemp[vizinho].append(v) # Adiciona a aresta inversa
                else:
                    adj_listTemp[v].append(aresta)
                    adj_listTemp[aresta].append(v)
    else:
        adj_listTemp = grafo.adj_list

    # Escolhe o primeiro vértice da lista de vértices para começar a DFS
    vertice_inicial = list(grafo.vertices.keys())[0]

    # Realiza a DFS a partir do vértice inicial
    visitados = set()
    DFS(grafo, vertice_inicial, adj_listTemp, visitados)

    # Verifica se todos os vértices foram alcançados
    return 1 if len(visitados) == len(grafo.vertices) else 0



# ------- Bipartido
def Bipartido(grafo):

    # A lógica é a mesma da DFS, mas a personalização é feita para colorir os vértices adjacentes com cores diferentes para identificar se o grafo é bipartido
    def verificar_bipartido(grafo, v, visitado, cor, current_color):
        cor[v] = current_color
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if cor[vizinho] == -1:
                if not verificar_bipartido(grafo, vizinho, visitado, cor, 1 - current_color): # Se o vértice vizinho não foi visitado aplicamos a DFS nele
                    return False
            elif cor[vizinho] == cor[v]: # Se o vértice vizinho tem a mesma cor que o vértice atual
                return False
        return True

    cor = {v: -1 for v in grafo.vertices}

    for vertice in grafo.vertices:
        if cor[vertice] == -1:
            if not verificar_bipartido(grafo, vertice, set(), cor, 0):
                return "0"

    return "1"


# ------- Euleriano
def Euleriano(grafo):
    if not Conexo(grafo): # Se o grafo não é conexo, ele não pode ser euleriano
        return "0"
    
    if grafo.direcionado:
        # Verifica se o grafo direcionado é euleriano (grau de entrada = grau de saída)
        grauEntrada = {v: 0 for v in grafo.vertices}
        grauSaida = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[1]
                grauSaida[v] += 1
                grauEntrada[vizinho] += 1
        
        # Verifica se os graus de entrada e saída são iguais para todos os vértices
        for v in grafo.vertices:
            if grauEntrada[v] != grauSaida[v]:
                return "0"
            
        return "1"

    else:
        # Verifica se o grafo não direcionado é euleriano
        grau = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau[v] += 1
        
        # Verifica se o grau de todos os vértices é par
        for v in grafo.vertices:
            if grau[v] % 2 != 0:
                return "0"
            
        return "1"


# ------- Procura Ciclos
def Cíclico(grafo):

    def verificarCiclo(grafo, v, visitado, pai):
        visitado.add(v) # Adiciona o vértice atual à lista de visitados
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if vizinho not in visitado:
                if verificarCiclo(grafo, vizinho, visitado, v):
                    return True
            elif vizinho != pai: # Se o vértice vizinho já foi visitado e não é o pai do vértice atual, então encontramos um ciclo 
                return True
        return False

    visitado = set() # Lista de vértices visitados
    
    for vertice in grafo.vertices:
        if vertice not in visitado:
            if verificarCiclo(grafo, vertice, visitado, None):
                return "1"
    return "0"


# ----- Funções Listar -----

# ------- Componentes Conexas
def ComponentesConexas(grafo):
    if grafo.direcionado:
        return -1
    
    # Inicializa a lista de componentes e o conjunto de vértices visitados
    componentes = []
    visitados = set()

    def dfsComponente(v, componenteAtual):
        visitados.add(v)
        componenteAtual.append(v) # Adiciona o vértice atual ao componente
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):  # Arestas como tuplas
                vizinho = vizinho[1] 
            if vizinho not in visitados:
                dfsComponente(vizinho, componenteAtual)

    for vertice in grafo.vertices:
        if vertice not in visitados:
            componenteAtual = []
            dfsComponente(vertice, componenteAtual)
            componentes.append(sorted(componenteAtual))  # Ordena para garantir a ordem correta

    return len(componentes) # Retorna o número de componentes conexas


# ------- Componentes Fortemente Conexas
def ComponentesFortementeConexas(grafo):

    if not grafo.direcionado:
        return -1
    # Algortimo de Kosaraju para encontrar componentes fortemente conexas
    def dfsGrafo_Original(v, visitados, stack):
        visitados.add(v)
        for item in grafo.adj_list.get(v, []):
            vizinho = item[1] if isinstance(item, tuple) else item
            if vizinho not in visitados:
                dfsGrafo_Original(vizinho, visitados, stack)
        stack.append(v) # Adiciona o vértice à pilha

    def dfsGrafo_alterado(v, visitados, componente_atual):
        visitados.add(v)
        componente_atual.append(v)
        for item in grafo.adj_list.get(v, []):
            vizinho = item[1] if isinstance(item, tuple) else item
            if vizinho not in visitados:
                dfsGrafo_alterado(vizinho, visitados, componente_atual)

    def inverterArestas():
        novaAadj_list = defaultdict(list)
        for v in grafo.adj_list:
            for item in grafo.adj_list[v]:
                vizinho = item[1] if isinstance(item, tuple) else item
                novaAadj_list[vizinho].append((item[0], v, item[2]) if isinstance(item, tuple) else (item[0], v))
        grafo.adj_list = dict(novaAadj_list)

    # Passo 1: Fazer uma DFS no grafo original para determinar a ordem de finalização dos vértices
    stack = []
    visitados = set()

    for vertice in grafo.vertices:
        if vertice not in visitados:
            dfsGrafo_Original(vertice, visitados, stack)

    # Passo 2: Inverter as arestas do grafo
    inverterArestas()
    
    # Passo 3: Fazer uma DFS na ordem inversa da finalização
    visitados.clear()
    componentes = []

    while stack:
        v = stack.pop() # Remove o último vértice da pilha
        if v not in visitados:
            componente_atual = [] 
            dfsGrafo_alterado(v, visitados, componente_atual)
            componentes.append(componente_atual) #armazena todos os vértices alcançados a partir de v

    # Restaurar o grafo original invertendo as arestas novamente
    inverterArestas()

    return len(componentes)


# ------- Trilha Euleriana
def listarCaminhoEuleriano(grafo):
    grau_saida = {v: 0 for v in grafo.vertices}
    grau_entrada = {v: 0 for v in grafo.vertices}

    def tem_caminho_euleriano_direcionado():
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau_saida[v] += 1
                grau_entrada[vizinho] += 1

        for v in grafo.vertices:
            if grau_saida[v] != grau_entrada[v]:
                return False

        return True

    def tipo_caminho_euleriano_nao_direcionado():
        grau_impar = 0
        for v in grafo.vertices:
            grau = len([vizinho for vizinho in grafo.adj_list[v] if isinstance(vizinho, tuple) or isinstance(vizinho, str)])
            if grau % 2 != 0:
                grau_impar += 1
        if grau_impar == 0:
            return "Euleriano"
        elif grau_impar == 2:
            return "Semi-Euleriano"
        else:
            return "Nenhum"

    if grafo.direcionado:
        if not tem_caminho_euleriano_direcionado():
            return "O grafo não tem um caminho euleriano."
        
        caminho = []
        stack = []
        u = next((v for v in grafo.vertices if grau_saida[v] - grau_entrada[v] == 1), None) or grafo.vertices[0]

        while stack or u is not None:
            if not grafo.adj_list[u]:
                caminho.append(u)
                u = stack.pop() if stack else None
            else:
                stack.append(u)
                u = grafo.adj_list[u].pop()[0] if isinstance(grafo.adj_list[u][-1], tuple) else grafo.adj_list[u].pop()

        return caminho[::-1]

    else:
        tipo_caminho = tipo_caminho_euleriano_nao_direcionado()
        if tipo_caminho == "Nenhum":
            return "O grafo não tem um caminho euleriano."

        caminho = []
        stack = []
        u = next((v for v in grafo.vertices if len(grafo.adj_list[v]) % 2 != 0), None) or grafo.vertices[0]
        arestas_usadas = set()

        while stack or u is not None:
            if not grafo.adj_list[u]:
                caminho.append(u)
                u = stack.pop() if stack else None
            else:
                encontrou_arestas = False
                for vizinho in grafo.adj_list[u]:
                    if isinstance(vizinho, tuple):
                        vizinho = vizinho[0]
                    if (u, vizinho) not in arestas_usadas and (vizinho, u) not in arestas_usadas:
                        stack.append(u)
                        arestas_usadas.add((u, vizinho))
                        arestas_usadas.add((vizinho, u))
                        u = vizinho
                        encontrou_arestas = True
                        break
                if not encontrou_arestas:
                    caminho.append(u)
                    u = stack.pop() if stack else None

        if tipo_caminho == "Euleriano":
            return caminho[::-1]
        elif tipo_caminho == "Semi-Euleriano":
            return "Caminho Semi-Euleriano: " + str(caminho[::-1])
        

# ------- Vértices de articulação
def VerticesArticulacao(grafo):
    if grafo.direcionado:
        return -1
    
    def dfs(v, tempo, parent=None):
        grafo.vertices[v].cor = 'cinza'
        grafo.vertices[v].tempo_descoberta = grafo.vertices[v].low = tempo
        tempo += 1
        filhos = 0
        eh_articulacao = False
        
        for _, vizinho, _ in grafo.adj_list[v]:
            if grafo.vertices[vizinho].cor == 'branco':
                filhos += 1
                grafo.vertices[vizinho].pai = v
                dfs(vizinho, tempo, v)
                
                grafo.vertices[v].low = min(grafo.vertices[v].low, grafo.vertices[vizinho].low)

                if parent is not None and grafo.vertices[vizinho].low >= grafo.vertices[v].tempo_descoberta:
                    eh_articulacao = True
            elif vizinho != parent:  # aresta de retorno
                grafo.vertices[v].low = min(grafo.vertices[v].low, grafo.vertices[vizinho].tempo_descoberta)

        if parent is None and filhos > 1:
            eh_articulacao = True

        if eh_articulacao:
            vertices_articulacao.append(v)

        grafo.vertices[v].cor = 'preto'

    vertices_articulacao = []
    tempo_inicial = 0
    
    # Inicializa as propriedades dos vértices
    for vertice in grafo.vertices:
        grafo.vertices[vertice].cor = 'branco'
        grafo.vertices[vertice].tempo_descoberta = -1
        grafo.vertices[vertice].low = -1
        grafo.vertices[vertice].pai = None
    
    for vertice in grafo.vertices:
        if grafo.vertices[vertice].cor == 'branco':
            dfs(vertice, tempo_inicial)
    
    return vertices_articulacao
    

# ------- Arestas Ponte
def ArestasPonte(grafo):
    if grafo.direcionado:
        return -1
    
    # Inicializa os dicionários
    vertices = grafo.vertices
    visitados = {v: False for v in vertices}
    descoberta = {v: float("inf") for v in vertices}
    baixo = {v: float("inf") for v in vertices}
    pai = {v: None for v in vertices}
    tempo = [0]
    pontes = []
    # Função de busca em profundidade com Algoritmo de Tarjan
    def dfsTarjan(v):
        visitados[v] = True
        tempo[0] += 1
        descoberta[v] = tempo[0]
        baixo[v] = tempo[0]

        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[1]

            if not visitados[vizinho]:
                pai[vizinho] = v
                dfsTarjan(vizinho)

                baixo[v] = min(baixo[v], baixo[vizinho]) # Atualiza o valor de 'baixo'

                # Se o vértice vizinho tem caminho de volta para 'v' na árvore de busca em profundidade, então a aresta (v, vizinho) é uma ponte
                if baixo[vizinho] > descoberta[v]:
                    pontes.append((v, vizinho))

            elif vizinho != pai[v]:
                baixo[v] = min(baixo[v], descoberta[vizinho])

    for v in vertices:
        if not visitados[v]:
            dfsTarjan(v)

    if not pontes:
        return 0
    else:
        return len(pontes)


# ----- Funções Gerar -----

# ------- Árvore de profundidade
def ArvoreProfundidade(grafo):
    def dfs(v, grafo, visitados, idArestas_usadas):
        visitados[v] = True
        for aresta in sorted(grafo.adj_list.get(v, []), key=lambda x: (x[1], x[0])):  # Ordena por vizinho e id_aresta
            id_aresta, vizinho = aresta[0], aresta[1]

            if not visitados[vizinho]: # Se o vizinho não foi visitado
                idArestas_usadas.append(id_aresta)  # Adiciona o identificador da aresta
                dfs(vizinho, grafo, visitados, idArestas_usadas)

    visitados = {v: False for v in grafo.vertices}
    idArestas_usadas = []
    dfs(0, grafo, visitados, idArestas_usadas)
    return idArestas_usadas


# ------- Árvore de largura
def ArvoreLargura(grafo):
    def bfs(v, grafo):
        visitados = {v: False for v in grafo.vertices}
        idArestas_usadas = []
        fila = deque([v])
        visitados[v] = True

        while fila:
            atual = fila.popleft() # Remove o primeiro elemento da fila
            for aresta in sorted(grafo.adj_list.get(atual,[]), key=lambda x: (x[1])):  # Ordena os vizinhos por ordem lexicográfica
                id_aresta, vizinho, *peso = aresta
            # adiciona os vizinhos à fila
                if not visitados[vizinho]:
                    visitados[vizinho] = True
                    fila.append(vizinho)
                    idArestas_usadas.append(id_aresta)

        return idArestas_usadas

    return bfs(0, grafo)


# ------- Árvore geradora mínima
def ArvoreGeradoraMinima(grafo):
    if grafo.direcionado:
        return -1

    # Inicializa estruturas de dados
    visitados = {v: False for v in grafo.vertices}
    minHeap = []
    totalPeso = 0
    inicial = next(iter(grafo.vertices))  # Começa com qualquer vértice

    # Marca o vértice inicial como visitado e adiciona suas arestas à heap, priorizando o menor peso
    visitados[inicial] = True
    for aresta in grafo.adj_list[inicial]:
        id_aresta, vizinho, peso = aresta
        heapq.heappush(minHeap, (peso, inicial, vizinho))

    while minHeap:
        # Remove a aresta com menor peso e adiciona o peso dela ao total
        peso, u, v = heapq.heappop(minHeap)
        if not visitados[v]:
            visitados[v] = True
            totalPeso += peso

            # Adiciona as arestas conectadas ao vértice 'v'
            for aresta in grafo.adj_list[v]:
                id_aresta, vizinho, peso = aresta
                if not visitados[vizinho]:
                    heapq.heappush(minHeap, (peso, v, vizinho))

    # Verifica se todos os vértices foram visitados
    if len(visitados) != len(grafo.vertices):
        return -1

    return totalPeso


# Ordem topológica 
def OrdemTopologica(grafo):
    # Verifica se o grafo é direcionado
    if not grafo.direcionado:
        return -1

    adj_list = grafo.adj_list
    pilha = []
    visitado = set()

    def dfs_pilha(grafo, v, tempo, adj_list, visitado, pilha):
        vertice = grafo.vertices[v]
        vertice.cor = 'cinza'
        tempo += 1
        vertice.tempo_descoberta = tempo

        for vizinho in adj_list.get(v,[]):
            if isinstance(vizinho, tuple):
                vizinho_id = vizinho[1]  
            else:
                vizinho_id = vizinho

            if vizinho_id not in visitado:
                visitado.add(vizinho_id)
                tempo = dfs_pilha(grafo, vizinho_id, tempo, adj_list, visitado, pilha) # Chama a DFS recursivamente aumentando o tempo

        # Quando não houver mais vizinhos, o vértice é finalizado e adicionado à pilha
        vertice.cor = 'preto'
        tempo += 1
        vertice.tempo_finalizacao = tempo

        pilha.append(v)
        return tempo

    for vertice in grafo.vertices:
        if vertice not in visitado:
            visitado.add(vertice)
            dfs_pilha(grafo, vertice, 0, adj_list, visitado, pilha)

    # A pilha contém os vértices na ordem inversa da ordem topológica
    return pilha[::-1]


# Valor do caminho mínimo entre dois vértices 
def CaminhoMinimo(grafo):
    # Verifica se todos os pesos das arestas são iguais
    pesos = set()
    for arestas in grafo.adj_list.values():
        for aresta in arestas:
            if isinstance(aresta, tuple):
                peso = aresta[2]  # O peso está no terceiro índice (índice 2)
            else:
                peso = 1  # Peso padrão para arestas não ponderadas
            pesos.add(peso)
            if len(pesos) > 1:  # Se encontrar mais de um peso, podemos parar
                break
        if len(pesos) > 1:
            break
    
    # Se todos os pesos forem iguais, retorna -1
    if len(pesos) == 1:
        return -1
    if grafo.direcionado:
        return -1

    origem = 0
    destino = len(grafo.vertices) - 1
    distancias = {v: float('inf') for v in grafo.vertices}
    distancias[origem] = 0
    heap = [(0, origem)]  # (distância, vértice)
    
    while heap:
        distancia_atual, vertice_atual = heapq.heappop(heap)
        
        if distancia_atual > distancias[vertice_atual]:
            continue
        
        for aresta in grafo.adj_list[vertice_atual]:
            if isinstance(aresta, tuple):
                vizinho = aresta[1]
                peso = aresta[2]  # O peso está no terceiro índice (índice 2)
            else:
                vizinho = aresta
                peso = 1  # Peso padrão para arestas não ponderadas
            
            nova_distancia = distancia_atual + peso
            
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                heapq.heappush(heap, (nova_distancia, vizinho))
    
    return distancias[destino] if distancias[destino] != float('inf') else -1


# Valor do fluxo máximo
def FluxoMaximo(grafo):
    origem = 0
    destino = len(grafo.vertices) - 1
    def bfs(capacidade_residual, origem, destino):
        fila = deque([origem])
        caminhos = {origem: []}

        while fila:
            u = fila.popleft()

            for v, capacidade in capacidade_residual[u].items():
                if v not in caminhos and capacidade > 0:
                    caminhos[v] = caminhos[u] + [(u, v)]
                    if v == destino:
                        return caminhos[v]
                    fila.append(v)

        return None

    if not grafo.direcionado:
        return -1
    
    capacidade_residual = defaultdict(dict)
    
    # Inicializa a capacidade residual do grafo
    for u in grafo.adj_list:
        for aresta in grafo.adj_list[u]:
            v, capacidade = aresta[1], aresta[2]
            capacidade_residual[u][v] = capacidade
            if v not in capacidade_residual:  # Adiciona o vértice v na capacidade_residual se não existir
                capacidade_residual[v] = defaultdict(int)
            capacidade_residual[v][u] = 0  # Inicializa a capacidade da aresta reversa com 0

    fluxo_maximo = 0
    caminho = bfs(capacidade_residual, origem, destino)

    while caminho:
        fluxo_caminho = min(capacidade_residual[u][v] for u, v in caminho)
        
        for u, v in caminho:
            capacidade_residual[u][v] -= fluxo_caminho
            capacidade_residual[v][u] += fluxo_caminho
        
        fluxo_maximo += fluxo_caminho
        caminho = bfs(capacidade_residual, origem, destino)
    
    return fluxo_maximo

# Fecho transitivo
def FechoTransitivo(grafo):
    if not grafo.direcionado:
        return -1
    # Inicializar o grafo de adjacência para o fecho transitivo
    adj_list = defaultdict(list)
    
    # Construir a lista de adjacência a partir da estrutura do grafo
    for u, adjacentes in grafo.adj_list.items():
        for aresta in adjacentes:
            # Considerar o segundo vértice da aresta (ignorar o idAresta e peso)
            v = aresta[1]
            adj_list[u].append(v)
    
    # O vértice inicial é 0
    vertice_inicial = 0
    visitados = set()
    fila = deque([vertice_inicial])
    
    while fila:
        u = fila.popleft()
        
        if u not in visitados:
            visitados.add(u)
            for v in sorted(adj_list[u]):
                if v not in visitados:
                    fila.append(v)
    
    # Excluir o próprio vértice inicial do fecho transitivo
    return sorted(v for v in visitados if v != vertice_inicial)


def ler_grafo():
    # Ler a lista de funções a serem executadas
    funcoes = list(map(int, input().strip().split()))
    
    # Ler a primeira linha com o número de vértices e arestas
    vertices_e_arestas = input().strip()
    num_vertices, num_arestas = map(int, vertices_e_arestas.split())
    
    # Gerar lista de vértices
    vertices = list(range(num_vertices))
    
    # Ler a segunda linha para saber se o grafo é direcionado ou não
    input_direcionado = input().strip().lower()
    direcionado = input_direcionado == 'direcionado'
    
    # Ler as arestas
    arestas = []
    for _ in range(num_arestas):
        aresta = input().strip()
        id_aresta, v1, v2, peso = map(int, aresta.split()) 

        if v1 not in vertices or v2 not in vertices:
            raise ValueError(f"Aresta referencia vértices fora do intervalo permitido: ({v1}, {v2})")
        arestas.append((id_aresta, v1, v2, peso))
    
    grafo = Grafo(vertices, arestas, direcionado)
    
    resultados = []
    for funcao in funcoes:
        if funcao == 0:
            resultados.append(Conexo(grafo))
        elif funcao == 1:
            resultados.append(Bipartido(grafo))
        elif funcao == 2:
            resultados.append(Euleriano(grafo))
        elif funcao == 3:
            resultados.append(Cíclico(grafo))
        elif funcao == 4:
            resultados.append(ComponentesConexas(grafo))
        elif funcao == 5:
            resultados.append(ComponentesFortementeConexas(grafo))
        # elif funcao == 6:
        #     resultados.append(listarCaminhoEuleriano(grafo))
        elif funcao == 6:
            resultados.append(VerticesArticulacao(grafo))
        elif funcao == 7:
            resultados.append(ArestasPonte(grafo))
        elif funcao == 8:
            resultados.append(ArvoreProfundidade(grafo))
        elif funcao == 9:
            resultados.append(ArvoreLargura(grafo))
        elif funcao == 10:
            resultados.append(ArvoreGeradoraMinima(grafo))
        elif funcao == 11:
            resultados.append(OrdemTopologica(grafo))
        elif funcao == 12:
            resultados.append(CaminhoMinimo(grafo))
        elif funcao == 13:
            resultados.append(FluxoMaximo(grafo))
        elif funcao == 14:
            resultados.append(FechoTransitivo(grafo))
        else:
            resultados.append(f"Função {funcao} não reconhecida.")
    
    return resultados

if __name__ == "__main__":
    try:
        resultados = ler_grafo()
        for resultado in resultados:
            print(resultado)
    except ValueError as e:
        print(f"Erro: {e}")
    # except Exception as e:
    #     print(f"Erro inesperado: {e}")
