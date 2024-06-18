import re

# Classe que representa um grafo
class Grafo:
    def __init__(self, vertices, arestas, direcionado=False):
        self.vertices = vertices
        self.arestas = arestas
        self.direcionado = direcionado
        self.adj_list = {v: [] for v in vertices}  # Cria um dicionário com cada vértice como chave e uma lista vazia como valor
        
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
        vertices_str = f'Vertices: {self.vertices}\n'
        arestas_str = 'Arestas: ['
        for i, (v1, v2, peso) in enumerate(self.arestas):
            if peso is not None:
                arestas_str += f'({v1}, {v2}, {peso})'
            else:
                arestas_str += f'({v1}, {v2})'
            if i < len(self.arestas) - 1:
                arestas_str += ', '
        arestas_str += ']\n'

        adj_list_str = 'Adjacency List:\n'
        for v in self.adj_list:
            if isinstance(self.adj_list[v][0], tuple):  # Verifica se a adjacência contém um tupla (vértice, peso)
                adj_list_str += f'{v}: {self.adj_list[v]}\n'
            else:
                adj_list_str += f'{v}: {self.adj_list[v]}\n'
        return vertices_str + arestas_str + adj_list_str


def ler_grafo_de_arquivo(filename, direcionado):
    with open(filename, 'r') as file:
        data = file.read().strip()  # Lê todo o conteúdo do arquivo e remove espaços em branco nas extremidades

    # Expressões regulares para extrair vértices e arestas
    vertices_pattern = r'V = \{([a-z,]+)\};'
    arestas_pattern = r'A = \{(.+?)\};'  # Alteração na expressão para capturar o conteúdo entre as chaves de arestas

    # Verificação de chaves de vértices
    if '{' not in data or '}' not in data:
        raise ValueError("Chaves de vértices não encontradas ou incorretamente formatadas.")

    vertices_match = re.search(vertices_pattern, data)  # Procura por correspondências no padrão de vértices
    arestas_match = re.search(arestas_pattern, data)  # Procura por correspondências no padrão de arestas

    if not vertices_match:
        raise ValueError("O arquivo não segue o formato esperado para vértices.")
    if not arestas_match:
        raise ValueError("O arquivo não segue o formato esperado para arestas.")

    vertices = vertices_match.group(1).split(',')  # Captura e separa os vértices
    arestas_raw = arestas_match.group(1)  # Conteúdo entre as chaves de arestas

    # Encontrar todas as arestas válidas usando expressão regular
    arestas_list = re.findall(r'\(\s*([a-z]),\s*([a-z])(?:,\s*(-?\d+))?\s*\)', arestas_raw)

    arestas = []
    for v1, v2, peso in arestas_list:
        v1 = v1.strip()
        v2 = v2.strip()
        peso = int(peso) if peso else None

        # Verificar se os vértices pertencem ao conjunto de vértices do grafo
        if v1 not in vertices or v2 not in vertices:
            raise ValueError(f"Aresta vai para vértices que não pertencem ao grafo: ({v1},{v2},{peso})")

        if direcionado:
            arestas.append((v1, v2, peso))  # Aresta direcionada
        else:
            arestas.append((v1, v2, peso))  # Aresta bidirecional

    return vertices, arestas


# Função para validar e criar o grafo
def criar_grafo_de_arquivo(filename, direcionado):
    vertices, arestas = ler_grafo_de_arquivo(filename, direcionado)  # Lê os vértices e arestas do arquivo
    grafo = Grafo(vertices, arestas, direcionado)  # Cria o grafo com os vértices e arestas lidos
    return grafo

# Exemplo de uso
if __name__ == "__main__":
    # Pergunta ao usuário se o grafo é direcionado ou não
    while True:
        resposta = input("O grafo é direcionado? (sim/não): ").strip().lower()
        if resposta in ['sim', 's']:
            direcionado = True
            break
        elif resposta in ['não', 'nao', 'n']:
            direcionado = False
            break
        else:
            print("Resposta inválida. Por favor, responda 'sim' ou 'não'.\n")

    # Substitua pelo caminho absoluto do seu arquivo
    filename = 'C:/Users/accn2/Documents/Grafos/analises-em-grafos/Ler-MontarGrafo/grafo.txt'
    try:
        grafo = criar_grafo_de_arquivo(filename, direcionado)
        print(grafo)  # Imprime a representação do grafo
    except ValueError as e:
        print(f"Erro: {e}")  # Imprime a mensagem de erro em caso de formato inválido
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")  # Imprime a mensagem de erro em caso de arquivo não encontrado
