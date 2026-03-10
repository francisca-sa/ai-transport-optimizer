import heapq
import time
from queue import Queue, LifoQueue
from combustivel import calcular_distancia

def bfs(G, origem, destino, num_passageiros, tempo_limite=None):
    start_time = time.time()
    visited = set()
    fila = Queue()
    fila.put(origem)
    visited.add(origem)
    parent = {origem: None}
    
    while not fila.empty():
        nodo_atual = fila.get()
        if nodo_atual == destino:
            break
        for vizinho in G.neighbors(nodo_atual):
            if vizinho not in visited:
                visited.add(vizinho)
                parent[vizinho] = nodo_atual
                fila.put(vizinho)
    
    path = []
    if destino in parent:
        node = destino
        while node is not None:
            path.append(node)
            node = parent.get(node)
        path.reverse()
    
    exec_time = round(time.time() - start_time, 4)
    return ([path] if path and path[0] == origem else []), exec_time

def dfs(G, origem, destino, num_passageiros, tempo_limite=None):
    start_time = time.time()
    stack = LifoQueue()
    stack.put((origem, [origem]))
    visited = set()
    resultado = []
    
    while not stack.empty():
        node, path = stack.get()
        if node == destino:
            resultado = [path]
            break
        if node not in visited:
            visited.add(node)
            for vizinho in G.neighbors(node):
                if vizinho not in visited:
                    stack.put((vizinho, path + [vizinho]))
    
    exec_time = round(time.time() - start_time, 4)
    return resultado, exec_time

def ucs(G, origem, destino, num_passageiros, tempo_limite=None):
    start_time = time.time()
    fila_prioridade = [(0, origem, [])]
    visitados = set()
    resultado = []
    
    while fila_prioridade:
        custo, node, path = heapq.heappop(fila_prioridade)
        if node in visitados:
            continue
        path = path + [node]
        if node == destino:
            resultado = [path]
            break
        visitados.add(node)
        for vizinho in G.neighbors(node):
            if vizinho not in visitados:
                custo_vizinho = custo + G[node][vizinho].get('custo', 0)
                heapq.heappush(fila_prioridade, (custo_vizinho, vizinho, path))
    
    exec_time = round(time.time() - start_time, 4)
    return resultado, exec_time

def a_star(G, origem, destino, pos, num_passageiros, tempo_limite=None):
    start_time = time.time()
    
    def heuristic(n):
        lat1, lon1 = pos[n]
        lat2, lon2 = pos[destino]
        return calcular_distancia(lat1, lon1, lat2, lon2)
    
    fila_prioridade = [(0 + heuristic(origem), 0, origem, [])]
    visitados = set()
    resultado = []
    
    while fila_prioridade:
        f, custo, node, path = heapq.heappop(fila_prioridade)
        if node in visitados:
            continue
        path = path + [node]
        if node == destino:
            resultado = [path]
            break
        visitados.add(node)
        for vizinho in G.neighbors(node):
            if vizinho not in visitados:
                novo_custo = custo + G[node][vizinho].get('custo', 0)
                heuristica_vizinho = heuristic(vizinho)
                heapq.heappush(fila_prioridade, (novo_custo + heuristica_vizinho, novo_custo, vizinho, path))
    
    exec_time = round(time.time() - start_time, 4)
    return resultado, exec_time

def greedy(G, origem, destino, pos, num_passageiros, tempo_limite=None):
    start_time = time.time()
    
    def heuristic(n):
        lat1, lon1 = pos[n]
        lat2, lon2 = pos[destino]
        return calcular_distancia(lat1, lon1, lat2, lon2)
    
    fila_prioridade = [(heuristic(origem), origem, [])]
    visitados = set()
    resultado = []
    
    while fila_prioridade:
        heur, node, path = heapq.heappop(fila_prioridade)
        if node in visitados:
            continue
        path = path + [node]
        if node == destino:
            resultado = [path]
            break
        visitados.add(node)
        for vizinho in G.neighbors(node):
            if vizinho not in visitados:
                heapq.heappush(fila_prioridade, (heuristic(vizinho), vizinho, path))
    
    exec_time = round(time.time() - start_time, 4)
    return resultado, exec_time