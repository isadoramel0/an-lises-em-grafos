def listarVertices(grafo):
    return list(grafo.vertices)

def listarArestas(grafo):
    arestas = 'Arestas: ['
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
                if vizinho not in visitados:
                    dfs(vizinho, stack)
            stack.append(v)

        def dfs_invertido(v, componente_atual):
            visitados.add(v)
            componente_atual.append(v)
            for vizinho in grafo.adj_list_reverso[v]:
                if vizinho not in visitados:
                    dfs_invertido(vizinho, componente_atual)

        stack = []
        for vertice in grafo.vertices:
            if vertice not in visitados:
                dfs(vertice, stack)

        grafo.inverter_arestas()  # Inverte as arestas para o grafo original
        visitados.clear()

        while stack:
            v = stack.pop()
            if v not in visitados:
                componente_atual = []
                dfs_invertido(v, componente_atual)
                componentes.append(componente_atual)

        grafo.inverter_arestas()  # Restaura as arestas originais do grafo

    else:
        # Componentes conexas para grafos não direcionados
        def dfs(v, componente_atual):
            visitados.add(v)
            componente_atual.append(v)
            for vizinho in grafo.adj_list[v]:
                if vizinho not in visitados:
                    dfs(vizinho, componente_atual)

        for vertice in grafo.vertices:
            if vertice not in visitados:
                componente_atual = []
                dfs(vertice, componente_atual)
                componentes.append(componente_atual)

    return componentes
