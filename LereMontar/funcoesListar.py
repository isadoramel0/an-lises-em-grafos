def DFS(grafo, v, tempo, adj_list):
    vertice = grafo.vertices[v]
    vertice.cor = 'cinza'
    tempo += 1
    vertice.tempo_descoberta = tempo

    for vizinho in adj_list[v]:
        if isinstance(vizinho, tuple):
            vizinho_id = vizinho[1]  # Acessa o vértice destino na tupla (idAresta, vizinho, peso)
        else:
            vizinho_id = vizinho

        vizinho_obj = grafo.vertices[vizinho_id]
        if vizinho_obj.cor == 'branco':
            vizinho_obj.pai = v
            tempo = DFS(grafo, vizinho_id, tempo, adj_list)

    vertice.cor = 'preto'
    tempo += 1
    vertice.tempo_finalizacao = tempo

    return tempo


# ------- Componentes Conexas
def ComponentesConexas(grafo):
    if grafo.direcionado:
        return -1
    
    componentes = []
    visitados = set()

    def dfs_componente(v, componente_atual):
        visitados.add(v)
        componente_atual.append(v)
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):  # Arestas como tuplas
                vizinho = vizinho[1]  # Seleciona apenas o vértice de destino
            if vizinho not in visitados:
                dfs_componente(vizinho, componente_atual)

    for vertice in grafo.vertices:
        if vertice not in visitados:
            componente_atual = []
            dfs_componente(vertice, componente_atual)
            componentes.append(sorted(componente_atual))  # Ordena para garantir a ordem correta

    return len(componentes)


# ------- Componentes Fortemente Conexas

def ComponentesFortementeConexas(grafo):
    if not grafo.direcionado:
        return -1

    def dfs_primeira_passagem(v, visitados, stack):
        visitados.add(v)
        for item in grafo.adj_list.get(v, []):
            vizinho = item[1] if isinstance(item, tuple) else item
            if vizinho not in visitados:
                dfs_primeira_passagem(vizinho, visitados, stack)
        stack.append(v)

    def dfs_segunda_passagem(v, visitados, componente_atual):
        visitados.add(v)
        componente_atual.append(v)
        for item in grafo.adj_list.get(v, []):
            vizinho = item[1] if isinstance(item, tuple) else item
            if vizinho not in visitados:
                dfs_segunda_passagem(vizinho, visitados, componente_atual)

    def inverter_arestas():
        novo_adj_list = defaultdict(list)
        for v in grafo.adj_list:
            for item in grafo.adj_list[v]:
                vizinho = item[1] if isinstance(item, tuple) else item
                novo_adj_list[vizinho].append((item[0], v, item[2]) if isinstance(item, tuple) else (item[0], v))
        grafo.adj_list = dict(novo_adj_list)

    # Passo 1: Fazer uma DFS no grafo original para determinar a ordem de finalização dos vértices
    stack = []
    visitados = set()

    for vertice in grafo.vertices:
        if vertice not in visitados:
            dfs_primeira_passagem(vertice, visitados, stack)

    # Passo 2: Inverter as arestas do grafo
    inverter_arestas()
    
    # Passo 3: Fazer uma DFS na ordem inversa da finalização
    visitados.clear()
    componentes = []

    while stack:
        v = stack.pop()
        if v not in visitados:
            componente_atual = []
            dfs_segunda_passagem(v, visitados, componente_atual)
            componentes.append(componente_atual)

    # Restaurar o grafo original invertendo as arestas novamente
    inverter_arestas()

    return len(componentes)


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
        

def encontrar_vertices_articulacao(grafo):
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
    for vertice in grafo.vertices:
        if grafo.vertices[vertice].cor == 'branco':
            dfs(vertice, tempo_inicial)
    
    return vertices_articulacao
    

def listarArestasPonte(grafo):
    # Inicializa os dicionários
    vertices = grafo.vertices
    visitados = {v: False for v in vertices}
    descoberta = {v: float("inf") for v in vertices}
    baixo = {v: float("inf") for v in vertices}
    pai = {v: None for v in vertices}
    tempo = [0]
    pontes = []
    # Função de busca em profundidade com Algoritmo de Tarjan
    def dfs(v):
        visitados[v] = True
        tempo[0] += 1
        descoberta[v] = tempo[0]
        baixo[v] = tempo[0]

        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]

            if not visitados[vizinho]:
                pai[vizinho] = v
                dfs(vizinho)

                baixo[v] = min(baixo[v], baixo[vizinho])

                # Verifica se (v, vizinho) é uma ponte
                if baixo[vizinho] > descoberta[v]:
                    pontes.append((v, vizinho))

            elif vizinho != pai[v]:
                baixo[v] = min(baixo[v], descoberta[vizinho])

    for v in vertices:
        if not visitados[v]:
            dfs(v)

    if not pontes:
        return "O grafo não possui arestas de ponte."
    else:
        return len(pontes)

def dfs_lexicografica(v, grafo, visitados, arestas_usadas):
    visitados[v] = True
    for aresta in sorted(grafo.adj_list[v], key=lambda x: (x[1], x[0])):  # Ordena por vizinho e id_aresta
        id_aresta, vizinho = aresta[0], aresta[1]
        
        if not visitados[vizinho]:
            arestas_usadas.append(id_aresta)  # Adiciona o identificador da aresta
            dfs_lexicografica(vizinho, grafo, visitados, arestas_usadas)

def arvore_lexicografica(grafo):
    visitados = {v: False for v in grafo.vertices}
    arestas_usadas = []
    dfs_lexicografica(0, grafo, visitados, arestas_usadas)
    return arestas_usadas

from collections import deque

def bfs_lexicografica(v, grafo):
    visitados = {v: False for v in grafo.vertices}
    arestas_usadas = []
    fila = deque([v])
    visitados[v] = True

    while fila:
        atual = fila.popleft()
        for aresta in sorted(grafo.adj_list[atual], key=lambda x: (x[1])):  # Ordena os vizinhos por ordem lexicográfica
            id_aresta, vizinho, *peso = aresta
            
            if not visitados[vizinho]:
                visitados[vizinho] = True
                fila.append(vizinho)
                arestas_usadas.append(id_aresta)

    return arestas_usadas

def arvore_largura(grafo):
    if 0 not in grafo.vertices:
        return []  # Se não há vértice 0 no grafo, não pode gerar a árvore de largura
    
    return bfs_lexicografica(0, grafo)

import heapq

import heapq

def arvore_geradora_minima(grafo):
    if grafo.direcionado:
        return -1

    # Inicializa estruturas de dados
    visitados = {v: False for v in grafo.vertices}
    min_heap = []
    total_peso = 0
    inicial = next(iter(grafo.vertices))  # Começa com qualquer vértice

    # Marca o vértice inicial como visitado e adiciona suas arestas à heap
    visitados[inicial] = True
    for aresta in grafo.adj_list[inicial]:
        id_aresta, vizinho, peso = aresta
        heapq.heappush(min_heap, (peso, inicial, vizinho))

    while min_heap:
        peso, u, v = heapq.heappop(min_heap)
        if not visitados[v]:
            visitados[v] = True
            total_peso += peso

            # Adiciona as arestas conectadas ao vértice 'v'
            for aresta in grafo.adj_list[v]:
                id_aresta, vizinho, peso = aresta
                if not visitados[vizinho]:
                    heapq.heappush(min_heap, (peso, v, vizinho))

    # Verifica se todos os vértices foram visitados
    if len(visitados) != len(grafo.vertices):
        return -1

    return total_peso


def ordem_topologica(grafo):
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

        for vizinho in adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho_id = vizinho[1]  # Acessa o vértice destino na tupla (idAresta, vizinho, peso)
            else:
                vizinho_id = vizinho

            if vizinho_id not in visitado:
                visitado.add(vizinho_id)
                tempo = dfs_pilha(grafo, vizinho_id, tempo, adj_list, visitado, pilha)

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

def caminho_minimo(grafo):
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


from collections import deque, defaultdict

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

def valor_fluxo_maximo(grafo, origem, destino):
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


from collections import defaultdict, deque

def fecho_transitivo(grafo):
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