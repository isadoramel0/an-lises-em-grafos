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

    def __repr__(self):
        vertices_str = 'Vertices: ('
        for vertice in self.vertices.values():
            vertices_str += f'{vertice.id}, '
        vertices_str += ')\n'

        arestas_str = 'Arestas: ['
        for i, (id_aresta, v1, v2, peso) in enumerate(self.arestas):
            if peso is not None:
                arestas_str += f'({id_aresta}, {v1}, {v2}, {peso})'
            else:
                arestas_str += f'({id_aresta}, {v1}, {v2})'
            if i < len(self.arestas) - 1:
                arestas_str += ', '
        arestas_str += ']\n'

        adj_list_str = 'Lista de Adjacencia:\n'
        for v in self.adj_list:
            adj_list_str += f'{v}: {self.adj_list[v]}\n'
        return vertices_str + arestas_str + adj_list_str
    
    def inverter_arestas(self):
        self.adj_list_reverso = {v: [] for v in self.vertices}
        for v in self.vertices:
            for vizinho in self.adj_list[v]:
                if isinstance(vizinho, tuple):  # Aresta ponderada
                    self.adj_list_reverso[vizinho[1]].append((v, vizinho[2]))
                else:  # Aresta não ponderada
                    self.adj_list_reverso[vizinho].append(v)

        self.adj_list, self.adj_list_reverso = self.adj_list_reverso, self.adj_list


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


# ----- Funções Verificar -----

# ------- Conexo
def Conexo(grafo):
    # Se o grafo é direcionado, criamos uma lista de adjacência temporária com arestas bidirecionais
    if grafo.direcionado:
        adj_list_temporaria = {v: [] for v in grafo.vertices}
        for v in grafo.adj_list:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    adj_list_temporaria[v].append(vizinho)
                    adj_list_temporaria[vizinho[0]].append((v, vizinho[1]))
                else:
                    adj_list_temporaria[v].append(vizinho)
                    adj_list_temporaria[vizinho].append(v)
    else:
        adj_list_temporaria = grafo.adj_list

    # Escolhe o primeiro vértice da lista de vértices para começar a DFS
    vertice_inicial = list(grafo.vertices.keys())[0]

    # Realiza a DFS a partir do vértice inicial usando a lista de adjacência apropriada
    tempo = 0
    DFS(grafo, vertice_inicial, tempo, adj_list_temporaria)

    # Verifica se todos os vértices foram alcançados
    if (all(grafo.vertices[vertice].cor == 'preto' for vertice in grafo.vertices)):
        return 1
    else:
        return 0


# ------- Bipartido
def Bipartido(grafo):
    def verificar_bipartido(grafo, v, visitado, cor, current_color):
        cor[v] = current_color
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if cor[vizinho] == -1:
                if not verificar_bipartido(grafo, vizinho, visitado, cor, 1 - current_color):
                    return False
            elif cor[vizinho] == cor[v]:
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
    if not Conexo(grafo):
        return "0"
    
    if grafo.direcionado:
        # Verifique se o grafo direcionado é euleriano
        grau_entrada = {v: 0 for v in grafo.vertices}
        grau_saida = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau_saida[v] += 1
                grau_entrada[vizinho] += 1
        
        # Verifique se os graus de entrada e saída são iguais para todos os vértices
        for v in grafo.vertices:
            if grau_entrada[v] != grau_saida[v]:
                return "0"
            
        return "1"

    else:
        # Verifique se o grafo não direcionado é euleriano
        grau = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau[v] += 1
        
        # Verifique se o grau de todos os vértices é par
        for v in grafo.vertices:
            if grau[v] % 2 != 0:
                return "0"
            
        return "1"


# ------- Procura ciclo
def Cíclico(grafo):
    def verificar_ciclo(grafo, v, visitado, pai):
        visitado.add(v)
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if vizinho not in visitado:
                if verificar_ciclo(grafo, vizinho, visitado, v):
                    return True
            elif vizinho != pai:
                return True
        return False

    visitado = set()
    
    for vertice in grafo.vertices:
        if vertice not in visitado:
            if verificar_ciclo(grafo, vertice, visitado, None):
                return "1"
    return "0"


# ----- Funções Listar -----

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
    

# ------- Arestas Ponte
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


# ----- Funções Gerar -----





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
        elif funcao == 6:
            resultados.append(listarCaminhoEuleriano(grafo))
        elif funcao == 7:
            resultados.append(encontrar_vertices_articulacao(grafo))
        elif funcao == 8:
            resultados.append(listarArestasPonte(grafo))
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
