def listarVertices(grafo):
    return list(grafo.vertices)


def listarArestas(grafo):
    arestas = '['
    for i, (v1, v2, peso) in enumerate(grafo.arestas):
        if peso is not None:
            arestas += f'({v1}, {v2}, {peso})'
        else:
            arestas += f'({v1}, {v2})'
        
        if i < len(grafo.arestas) - 1:
            arestas += ', '
        
    arestas += ']\n'
    return arestas


def listarComponentesConexas(grafo):
    componentes = []
    visitados = set()

    if grafo.direcionado:
        # Algoritmo de Kosaraju para componentes fortemente conexas
        def dfs(v, stack):
            visitados.add(v)
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                if vizinho not in visitados:
                    dfs(vizinho, stack)
            stack.append(v)

        def dfs_invertido(v, componente_atual):
            visitados.add(v)
            componente_atual.append(v)
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                if vizinho not in visitados:
                    dfs_invertido(vizinho, componente_atual)

        stack = []
        for vertice in grafo.vertices:
            if vertice not in visitados:
                dfs(vertice, stack)

        grafo.inverter_arestas()
        visitados.clear()

        while stack:
            v = stack.pop()
            if v not in visitados:
                componente_atual = []
                dfs_invertido(v, componente_atual)
                componentes.append(componente_atual)

        grafo.inverter_arestas()

    else:
        # Componentes conexas para grafos não direcionados
        def dfs(v, componente_atual):
            visitados.add(v)
            componente_atual.append(v)
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                if vizinho not in visitados:
                    dfs(vizinho, componente_atual)

        for vertice in grafo.vertices:
            if vertice not in visitados:
                componente_atual = []
                dfs(vertice, componente_atual)
                componentes.append(componente_atual)

    return componentes


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
        

def listarCaminhoHamiltoniano(grafo):
    n = len(grafo.vertices)
    
    def backtrack(v, caminho, visitados):
        if len(caminho) == n:
            if caminho[0] in [vizinho if not isinstance(vizinho, tuple) else vizinho[0] for vizinho in grafo.adj_list[v]]:
                caminho.append(caminho[0])
                return True
            else:
                return False

        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if vizinho not in visitados:
                visitados.add(vizinho)
                caminho.append(vizinho)
                if backtrack(vizinho, caminho, visitados):
                    return True
                visitados.remove(vizinho)
                caminho.pop()
        return False

    for start in grafo.vertices:
        caminho = [start]
        visitados = set([start])
        if backtrack(start, caminho, visitados):
            return caminho

    return "O grafo não tem um caminho Hamiltoniano."