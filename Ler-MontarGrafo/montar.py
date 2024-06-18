import re

# Classe que representa um grafo
class Grafo:
    def __init__(self, vertices, arestas):
        # Inicializa os vértices, as arestas e a lista de adjacências
        self.vertices = vertices
        self.arestas = arestas
        self.adj_list = {v: [] for v in vertices}  # Cria um dicionário com cada vértice como chave e uma lista vazia como valor
        for (v1, v2, peso) in arestas:
            self.adj_list[v1].append((v2, peso))  # Adiciona a aresta à lista de adjacências do vértice de partida
            if peso is not None:  # Só adiciona a aresta inversa se for ponderada
                self.adj_list[v2].append((v1, peso))  # Se for um grafo não direcionado, adiciona a aresta inversa

    def __repr__(self):
        # Método para representar o grafo como string
        vertices_str = f'Vertices: {self.vertices}\n'
        arestas_str = f'Arestas: {self.arestas}\n'
        adj_list_str = 'Lista de Adjacencia:\n'
        for v in self.adj_list:
            adj_list_str += f'{v}: {self.adj_list[v]}\n'
        return vertices_str + arestas_str + adj_list_str

def ler_grafo_de_arquivo(filename):
    with open(filename, 'r') as file:
        data = file.read().strip()  # Lê todo o conteúdo do arquivo e remove espaços em branco nas extremidades

    # Expressões regulares para extrair vértices e arestas
    vertices_pattern = r'V = \{([a-z,]+)\};'
    arestas_pattern = r'A = \{((?:\([a-z],[a-z],-?\d+\)|\([a-z],[a-z]\))(?:,(?:\([a-z],[a-z],-?\d+\)|\([a-z],[a-z]\)))*)\};'
    
    vertices_match = re.search(vertices_pattern, data)  # Procura por correspondências no padrão de vértices
    arestas_match = re.search(arestas_pattern, data)  # Procura por correspondências no padrão de arestas

    if not vertices_match:
        raise ValueError("O arquivo não segue o formato esperado para vértices.")
    if not arestas_match:
        raise ValueError("O arquivo não segue o formato esperado para arestas.")

    vertices = vertices_match.group(1).split(',')  # Captura e separa os vértices
    arestas = []

    # Debug: Verificar correspondência de arestas brutas
    print(f"Arestas brutas: {arestas_match.group(1)}")

    # Encontra todas as arestas no formato correto
    arestas_raw = arestas_match.group(1)
    arestas_list = re.findall(r'\([a-z],[a-z],-?\d+\)|\([a-z],[a-z]\)', arestas_raw)

    for aresta in arestas_list:
        partes = aresta.strip('()').split(',')  # Remove parênteses e divide a aresta em partes
        if len(partes) == 3:  # Grafo ponderado
            v1, v2, peso = partes[0], partes[1], int(partes[2])
        elif len(partes) == 2:  # Grafo não ponderado
            v1, v2, peso = partes[0], partes[1], None
        else:
            raise ValueError(f"O arquivo não segue o formato esperado para uma aresta: {aresta}")
        arestas.append((v1, v2, peso))  # Adiciona a aresta à lista de arestas

    # Verificação adicional para garantir que todos os vértices nas arestas estão na lista de vértices
    vertices_set = set(vertices)
    for (v1, v2, peso) in arestas:
        if v1 not in vertices_set or v2 not in vertices_set:
            raise ValueError("O arquivo contém arestas com vértices que não estão na lista de vértices.")

    return vertices, arestas

# Função para validar e criar o grafo
def criar_grafo_de_arquivo(filename):
    vertices, arestas = ler_grafo_de_arquivo(filename)  # Lê os vértices e arestas do arquivo
    grafo = Grafo(vertices, arestas)  # Cria o grafo com os vértices e arestas lidos
    return grafo

# Exemplo de uso
if __name__ == "__main__":
    # Substitua pelo caminho absoluto do seu arquivo
    filename = 'analises-em-grafos/Ler-MontarGrafo/grafo.txt'
    try:
        grafo = criar_grafo_de_arquivo(filename)
        print(grafo)  # Imprime a representação do grafo
    except ValueError as e:
        print(f"Erro: {e}")  # Imprime a mensagem de erro em caso de formato inválido
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")  # Imprime a mensagem de erro em caso de arquivo não encontrado
