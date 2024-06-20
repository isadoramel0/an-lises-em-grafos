from Ler_MontarGrafo.montar import criar_grafo_de_arquivo

if __name__ == "__main__":
    # pergunta ao usuário se o grafo é direcionado ou não;
    while True:
        resposta = input("O grafo é direcionado? (sim/não): ").strip().lower()
        if resposta in ['sim', 's', 'Sim', 'SIM']:
            direcionado = True
            break
        elif resposta in ['não', 'nao', 'n', 'Não', 'Nao', 'NAO', 'NÃO']:
            direcionado = False
            break
        else:
            print("Resposta inválida. Por favor, responda 'sim' ou 'não'.\n")

    
    filename = 'grafo.txt'
    try:
        # inicializa a criação e leitura do grafo;
        grafo = criar_grafo_de_arquivo(filename, direcionado)
        print(grafo) 
    except ValueError as e:
        print(f"Erro: {e}")  # erro no caso o formato seja inválido;
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")  # erro no caso de arquivo não encontrado;
