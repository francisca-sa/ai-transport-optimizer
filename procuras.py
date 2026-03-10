import networkx as nx
from itertools import islice
from algoritmos import bfs, dfs, ucs, a_star, greedy

def obter_caminhos(G, origem, destino, num_passageiros, pos=None, 
                  algoritmo='ucs', tempo_limite=None):
    if algoritmo == 'bfs':
        caminhos, tempo_exec = bfs(G, origem, destino, num_passageiros, tempo_limite)
    elif algoritmo == 'dfs':
        caminhos, tempo_exec = dfs(G, origem, destino, num_passageiros, tempo_limite)
    elif algoritmo == 'ucs':
        caminhos, tempo_exec = ucs(G, origem, destino, num_passageiros, tempo_limite)
    elif algoritmo == 'a_star':
        caminhos, tempo_exec = a_star(G, origem, destino, pos, num_passageiros, tempo_limite)
    elif algoritmo == 'greedy':
        caminhos, tempo_exec = greedy(G, origem, destino, pos, num_passageiros, tempo_limite)
    else:
        raise ValueError("Algoritmo não suportado")
    
    print(f"Tempo de execução do {algoritmo.upper()}: {tempo_exec} segundos")
    return caminhos

def obter_top_caminhos_por_custo(G, origem, destino, num_passageiros, num_caminhos=10):
    try:
        caminhos = list(islice(nx.shortest_simple_paths(G, origem, destino, weight='custo'), num_caminhos))
        return caminhos
    except nx.NetworkXNoPath:
        return []

def calcular_custo_total(G, caminho, num_passageiros):
    custo_total = 0
    custos_etapas = []
    
    for i in range(len(caminho) - 1):
        u, v = caminho[i], caminho[i+1]
        capacidade = G[u][v].get('capacidade')
        custo_por_pessoa = G[u][v].get('custo', 0)
        
        if capacidade is None or capacidade >= num_passageiros:
            custo_etapa = custo_por_pessoa * num_passageiros
            custo_por_pessoa_etapa = custo_por_pessoa
        else:
            viagens = (num_passageiros + capacidade - 1) // capacidade
            custo_etapa = custo_por_pessoa * num_passageiros
            custo_por_pessoa_etapa = custo_por_pessoa
        
        custo_total += custo_etapa
        custos_etapas.append(custo_por_pessoa_etapa)
    
    return custo_total, custos_etapas
