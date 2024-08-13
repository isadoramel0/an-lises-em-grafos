from LereMontar.menu import mostrar_menu_principal, obter_escolha, processar_escolha_principal

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
        
        for (v1, v2, peso) in arestas:
            if peso is not None:  # Grafo ponderado
                self.adj_list[v1].append((v2, peso))
                if not self.direcionado:
                    self.adj_list[v2].append((v1, peso))  # Aresta bidirecional
            else:  # Grafo não ponderado
                self.adj_list[v1].append(v2)
                if not self.direcionado:
                    self.adj_list[v2].append(v1)  # Aresta bidirecional

    def __repr__(self):
        vertices_str = 'Vertices: ('
        for vertice in self.vertices.values():
            vertices_str += f'{vertice.id}, '
        vertices_str += ')\n'

        arestas_str = 'Arestas: ['
        for i, (v1, v2, peso) in enumerate(self.arestas):
            if peso is not None:
                arestas_str += f'({v1}, {v2}, {peso})'
            else:
                arestas_str += f'({v1}, {v2})'
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
                    self.adj_list_reverso[vizinho[0]].append((v, vizinho[1]))
                else:  # Aresta não ponderada
                    self.adj_list_reverso[vizinho].append(v)

        self.adj_list, self.adj_list_reverso = self.adj_list_reverso, self.adj_list


def ler_grafo():
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
        arestas.append((v1, v2, peso))
    
    return Grafo(vertices, arestas, direcionado)


if __name__ == "__main__":
    try:
        # Inicializa a criação e leitura do grafo pelo terminal
        grafo = ler_grafo()
        print(grafo)

        while True:
            mostrar_menu_principal()
            escolha_principal = obter_escolha()
            if escolha_principal == '0':
                break
            processar_escolha_principal(escolha_principal, grafo)
        
    except ValueError as e:
        print(f"Erro: {e}")  # erro no caso de formato inválido;
    except Exception as e:
        print(f"Erro inesperado: {e}")  # para capturar qualquer outro erro inesperado.