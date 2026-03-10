import csv
import networkx as nx
import matplotlib.pyplot as plt
from combustivel import calcular_distancia

def carregar_grafo(caminho_csv="ligacoes.csv"):
    G = nx.Graph()
    pos = {}

    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            origem = row['origem']
            destino = row['destino']
            key = (origem, destino)


            tempo = int(row['tempo_viagem_minutos'])
            custo = float(row['custo_euros'])
            tipo = row['tipo_transporte'].strip()
            capacidade = int(row['capacidade']) if row['capacidade'].strip() else None
            intervalo=row['intervalo_minutos'].strip()
            primeira_partida=row['primeira_partida_hora'].strip()
            ultima_partida=row['ultima_partida_hora'].strip()

            lat1 = float(row['latitude_origem'])
            lon1 = float(row['longitude_origem'])
            lat2 = float(row['latitude_destino'])
            lon2 = float(row['longitude_destino'])
            distancia_km = calcular_distancia(lat1, lon1, lat2, lon2)

            G.add_edge(origem, destino,
                       tempo=tempo,
                       custo=custo,
                       tipo=tipo,
                       capacidade=capacidade,
                       distancia_km=distancia_km,
                       intervalo_minutos=intervalo,
                       primeira_partida_hora=primeira_partida,
                       ultima_partida_hora=ultima_partida)

            if origem not in pos:
                pos[origem] = (float(row['longitude_origem']), float(row['latitude_origem']))
            if destino not in pos:
                pos[destino] = (float(row['longitude_destino']), float(row['latitude_destino']))

    return G, pos

def desenhar_grafo(G, pos):
    nx.draw(G, pos, with_labels=True, node_size=200, font_size=6, 
            node_color='lightpink', edge_color='lightgrey', width=0.5)
    plt.title("Mapa de Conexões entre Estádios e Transportes", size=15)
    plt.show()

